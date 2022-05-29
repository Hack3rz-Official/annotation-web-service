import { SupportedLanguage } from '../../src/constants/supported-languages.enum';

export const getMockHighlightRequestDto = () => {
  return {
    code: 'class HelloWorld {\\n    private static void main(String[] args) {\\n        System.out.println(\\"Hello World!\\");\\n    }\\n}',
    language: SupportedLanguage.JAVA,
  };
};

export const getMockHCodeValues = () => [
  7, 10, 3, 6, 8, 8, 1, 10, 10, 5, 10, 8, 8, 3, 10, 10, 10, 10, 10, 10, 7, 3, 6,
  6, 6,
];
export const getMockLexingData = () => [
  { startIndex: 0, endIndex: 4, tokenId: 9 },
  { startIndex: 6, endIndex: 15, tokenId: 102 },
  { startIndex: 17, endIndex: 17, tokenId: 59 },
  { startIndex: 23, endIndex: 29, tokenId: 33 },
  { startIndex: 31, endIndex: 36, tokenId: 38 },
  { startIndex: 38, endIndex: 41, tokenId: 48 },
  { startIndex: 43, endIndex: 46, tokenId: 102 },
  { startIndex: 47, endIndex: 47, tokenId: 57 },
  { startIndex: 48, endIndex: 53, tokenId: 102 },
  { startIndex: 54, endIndex: 54, tokenId: 61 },
  { startIndex: 55, endIndex: 55, tokenId: 62 },
  { startIndex: 57, endIndex: 60, tokenId: 102 },
  { startIndex: 61, endIndex: 61, tokenId: 58 },
  { startIndex: 63, endIndex: 63, tokenId: 59 },
  { startIndex: 73, endIndex: 78, tokenId: 102 },
  { startIndex: 79, endIndex: 79, tokenId: 65 },
  { startIndex: 80, endIndex: 82, tokenId: 102 },
  { startIndex: 83, endIndex: 83, tokenId: 65 },
  { startIndex: 84, endIndex: 90, tokenId: 102 },
  { startIndex: 91, endIndex: 91, tokenId: 57 },
  { startIndex: 92, endIndex: 105, tokenId: 55 },
  { startIndex: 106, endIndex: 106, tokenId: 58 },
  { startIndex: 107, endIndex: 107, tokenId: 63 },
  { startIndex: 113, endIndex: 113, tokenId: 60 },
  { startIndex: 115, endIndex: 115, tokenId: 60 },
];

export const getMockResultHtml = () => `<!DOCTYPE html>
    <html>
    <style>
    .ANY {
        color: black;
        font-weight: normal;
        font-style: normal;
    }
    .KEYWORD {
        color: blue;
        font-weight: bold;
        font-style: normal;
    }
    .LITERAL {
        color: lightskyblue;
        font-weight: bold;
        font-style: normal;
    }
    .CHAR_STRING_LITERAL {
        color: darkgoldenrod;
        font-weight: normal;
        font-style: normal;
    }
    .COMMENT {
        color: grey;
        font-weight: normal;
        font-style: italic;
    }
    .CLASS_DECLARATOR {
        color: crimson;
        font-weight: bold;
        font-style: normal;
    }
    .FUNCTION_DECLARATOR {
        color: fuchsia;
        font-weight: bold;
        font-style: normal;
    }
    .VARIABLE_DECLARATOR {
        color: purple;
        font-weight: bold;
        font-style: normal;
    }
    .TYPE_IDENTIFIER {
        color: darkgreen;
        font-weight: bold;
        font-style: normal;
    }
    .FUNCTION_IDENTIFIER {
        color: dodgerblue;
        font-weight: normal;
        font-style: normal;
    }
    .FIELD_IDENTIFIER {
        color: coral;
        font-weight: normal;
        font-style: normal;
    }
    .ANNOTATION_DECLARATOR {
        color: lightslategray;
        font-weight: lighter;
        font-style: italic;
    }
    </style>
    <pre><code><span class='VARIABLE_DECLARATOR'>class</span> <span class='FIELD_IDENTIFIER'>HelloWorld</span> <span class='CHAR_STRING_LITERAL'>{</span>\\n   <span class='FUNCTION_DECLARATOR'> privat</span>e<span class='TYPE_IDENTIFIER'> stati</span>c<span class='TYPE_IDENTIFIER'> voi</span>d<span class='KEYWORD'> mai</span><span class='FIELD_IDENTIFIER'>n</span><span class='FIELD_IDENTIFIER'>(Strin</span><span class='CLASS_DECLARATOR'>g</span><span class='FIELD_IDENTIFIER'>[</span>]<span class='TYPE_IDENTIFIER'> arg</span><span class='TYPE_IDENTIFIER'>s</span>)<span class='CHAR_STRING_LITERAL'> </span>{\\n      <span class='FIELD_IDENTIFIER'>  Syst</span><span class='FIELD_IDENTIFIER'>e</span><span class='FIELD_IDENTIFIER'>m.o</span><span class='FIELD_IDENTIFIER'>u</span><span class='FIELD_IDENTIFIER'>t.print</span><span class='FIELD_IDENTIFIER'>l</span><span class='VARIABLE_DECLARATOR'>n(\\"Hello Worl</span><span class='CHAR_STRING_LITERAL'>d</span><span class='FUNCTION_DECLARATOR'>!</span>\\");\\<span class='FUNCTION_DECLARATOR'>n</span> <span class='FUNCTION_DECLARATOR'> </span>
    </code>
    </pre>
    </html>`;
