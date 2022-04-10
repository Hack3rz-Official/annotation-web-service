import os
from typing import Optional, Final, Tuple, List

import torch
import torch.nn.functional

# constants
# JAVA
# ---------------------------------
JAVA_LANG_NAME: Final[str] = 'java'
JAVA_LEXER_MAX_TOKEN_VAL: Final[int] = 107
# ---------------------------------
#
# KOTLIN
# ---------------------------------
KOTLIN_LANG_NAME: Final[str] = 'kotlin'
KOTLIN_LEXER_MAX_TOKEN_VAL: Final[int] = 176
#
# PYTHON3
# ---------------------------------
PYTHON3_LANG_NAME: Final[str] = 'python3'
PYTHON3_LEXER_MAX_TOKEN_VAL: Final[int] = 100

# From Kotlin's implementation:
ANY: Final[Tuple[int, str]] = (0, 'ANY')
#
KEYWORD: Final[Tuple[int, str]] = (1, 'KEYWORD')
LITERAL: Final[Tuple[int, str]] = (2, 'LITERAL')
CHAR_STRING_LITERAL: Final[Tuple[int, str]] = (3, 'CHAR_STRING_LITERAL')
COMMENT: Final[Tuple[int, str]] = (4, 'COMMENT')
#
CLASS_DECLARATOR: Final[Tuple[int, str]] = (5, 'CLASS_DECLARATOR')
FUNCTION_DECLARATOR: Final[Tuple[int, str]] = (6, 'FUNCTION_DECLARATOR')
VARIABLE_DECLARATOR: Final[Tuple[int, str]] = (7, 'VARIABLE_DECLARATOR')
#
TYPE_IDENTIFIER: Final[Tuple[int, str]] = (8, 'TYPE_IDENTIFIER')
FUNCTION_IDENTIFIER: Final[Tuple[int, str]] = (9, 'FUNCTION_IDENTIFIER')
FIELD_IDENTIFIER: Final[Tuple[int, str]] = (10, 'FIELD_IDENTIFIER')
#
ANNOTATION_DECLARATOR: Final[Tuple[int, str]] = (11, 'ANNOTATION_DECLARATOR')


class _BaseRNNClassifier(torch.nn.Module):
    """
    Base implementation of Recurrent Neural Network for sequence to sequence classification.
    """

    def __init__(self,
                 embedding_dim: int,
                 hidden_dim: int,
                 vocab_size: int,
                 tagset_size: int,
                 num_layers: int,
                 is_bidirectional: bool):
        """
        :param embedding_dim: Embedding layer dimension. A Dimension smaller than 1 removes the embedding layer.
        :param hidden_dim: Hidden layer dimension.
        :param vocab_size: Size of the vocabulary or input layer.
        :param tagset_size: Size of the target or output layer.
        :param num_layers: Number of hidden layers.
        :param is_bidirectional: Bidirectional.
        """
        super().__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size
        self.tagset_size = tagset_size
        self.num_layers = num_layers
        self.is_bidirectional = is_bidirectional
        #
        self.word_embeddings = torch.nn.Embedding(vocab_size, embedding_dim) if embedding_dim > 1 else None
        self.rnn = torch.nn.RNN(embedding_dim, hidden_dim, num_layers=num_layers, bidirectional=is_bidirectional)
        self.fc1 = torch.nn.Linear(hidden_dim * 2 if is_bidirectional else hidden_dim, tagset_size)

    def forward(self, seq):
        """
        Forward pass on RNN.
        :param seq: Tensor of normalised input token ids.
        :return: Log-SoftMax of the output layer's tensor if in training mode, else the output layer tensor.
        """
        n = len(seq)
        out = self.word_embeddings(seq) if self.word_embeddings is not None else seq.float()
        out = out.view(n, 1, -1)
        out, _ = self.rnn(out)
        if self.is_bidirectional:
            out = out[:, -1, :]
        else:
            out = out.view(n, -1)
        out = self.fc1(out)
        if not self.training:
            out = torch.nn.functional.log_softmax(out, dim=1)
        return out


class SHModel:
    """
    Handles the loading, fine-tuning, prediction and persisting of Syntax Highlighting base models.
    """

    def __init__(self, lang_name: str, model_name: str):
        """
        Creates a new model, or loads the model's latest state from disk if it exists.
        :param lang_name: The name of the target language as one of: JAVA_LANG_NAME,
        KOTLIN_LANG_NAME or PYTHON3_LANG_NAME
        :param model_name: Arbitrary name of the model, this will be used to save and load
        the model to disc, together with the name of the language.
        """
        torch.manual_seed(1)
        #
        self._config_name: str = f"{lang_name}_{model_name}"
        #
        if lang_name == JAVA_LANG_NAME:
            self._input_dim = JAVA_LEXER_MAX_TOKEN_VAL
        elif lang_name == KOTLIN_LANG_NAME:
            self._input_dim = KOTLIN_LEXER_MAX_TOKEN_VAL
        elif lang_name == PYTHON3_LANG_NAME:
            self._input_dim = PYTHON3_LEXER_MAX_TOKEN_VAL
        else:
            raise f"Unkown lang_name '{lang_name}'," \
                  f"options available: {[JAVA_LANG_NAME, KOTLIN_LANG_NAME, PYTHON3_LANG_NAME]}"
        #
        self._input_dim += 2  # '+2' refers to 'EOF' always '-1': all were added +1 before this stage.
        #
        self._embs_dim: int = 128
        self._hidden_dim: int = 32
        self._hidden_layers: int = 1
        self._is_bidirectional: bool = True
        #
        self._module_path: str = f"{self._config_name}.pt"
        #
        self._model = _BaseRNNClassifier(
            embedding_dim=self._embs_dim,
            vocab_size=self._input_dim,
            hidden_dim=self._hidden_dim,
            tagset_size=ANNOTATION_DECLARATOR[0] + 1,  # task_max_val is last index, hence + 1
            num_layers=self._hidden_layers,
            is_bidirectional=self._is_bidirectional
        )
        if os.path.exists(self._module_path):
            self._model.load_state_dict(torch.load(self._module_path, map_location='cpu'))
        else:
            self.persist_model()
        #
        self._optimiser: Optional[torch.optim.Adam] = None
        self._loss_func: Optional[torch.nn.modules.loss.CrossEntropyLoss] = None

    def persist_model(self):
        """
        Saves the model to disk in './<lang-name>_<model_name>.pt'. Thereby making it
        loadable from disk during the initialisation of a SHModel object, for the same
        lang_name and model_name values.
        """
        self._model.zero_grad()
        torch.save(self._model.state_dict(), self._module_path)

    def setup_for_prediction(self):
        """
        Prepares the model for prediction. A model only needs to be
        setup once during its lifetime, even after multiple predictions.
        """
        self._optimiser = None
        self._loss_func = None
        self._model.zero_grad()
        self._model.eval()

    def setup_for_finetuning(self):
        """
        Prepares the model for fine-tuning.A model only needs to be
        setup once during its lifetime, even after multiple fine-tuning steps.
        """
        self._model.train()
        self._optimiser = torch.optim.Adam(self._model.parameters(), lr=1e-4)
        self._loss_func = torch.nn.CrossEntropyLoss()

    def finetune_on(self, tok_ids: List[int], h_codes: List[int]) -> float:
        """
        Attempts to finetune the prediction logic of the model by learning from
        the example provided.
        :param tok_ids: The sequence of token rule ids, as naturally specified by the
        selected language name. Its length must be non-zero and be equal to the length
        of the h_codes provided.
        :param h_codes: The sequence of target syntax highlighting codes.  Its length must
        be non-zero and be equal to the length of the tok_ids provided.
        """
        assert self._optimiser is not None
        assert self._loss_func is not None
        assert self._model is not None
        assert len(tok_ids) == len(h_codes)
        assert len(tok_ids) > 0
        #
        self._optimiser.zero_grad()
        self._loss_func.zero_grad()
        self._model.zero_grad()
        #
        n_tok_ids = list(map(lambda i: int(i) + 1, tok_ids))
        x = torch.tensor(n_tok_ids, dtype=torch.long)
        #
        y = torch.tensor(h_codes, dtype=torch.long)
        #
        t = self._model(x)
        loss = self._loss_func(t, y)
        loss.backward()
        self._optimiser.step()
        #
        self._optimiser.zero_grad()
        self._loss_func.zero_grad()
        self._model.zero_grad()

        return loss.item()

    def predict(self, tok_ids: List[int]) -> List[int]:
        """
        :param tok_ids: The sequence of token rule ids, as naturally specified by the
        selected language name.
        :returns: The predicted sequence of syntax highlighting codes.
        """
        if len(tok_ids) == 0:
            return []
        else:
            x = self._tok_ids_to_model_input(tok_ids)
            ps = torch.argmax(self._model(x), dim=1)
            return list([int(thc.item()) for thc in ps])

    @staticmethod
    def _tok_ids_to_model_input(tok_ids: List[int]) -> torch.Tensor:
        n_tok_ids = list(map(lambda i: int(i) + 1, tok_ids))
        return torch.tensor(n_tok_ids, dtype=torch.long)
