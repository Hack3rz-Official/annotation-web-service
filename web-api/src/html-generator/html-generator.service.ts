import { Injectable } from '@nestjs/common';
import { HCodes } from '../constants/hcodes.enum';
import { HighlightRequestDto } from '../modules/highlight/dto/highlight-request.dto';

@Injectable()
export class HtmlGeneratorService {
  /**
   * This method builds the complete html document that is returned to the client.
   * It takes the request dto together with the prediction and lexing results and builds
   * a pre-styled html document with the corresponding css style definitions.
   * @param {HighlightRequestDto} highlightRequestDto The request dto containing the language and the code to be highlighted.
   * @param {Array<any>} lexingData The data returned by the lexing service.
   * @param {Array<any>} hCodeValues An array containing the h code values from the prediction service.
   */
  buildHtml(
    highlightRequestDto: HighlightRequestDto,
    lexingData: Array<any>,
    hCodeValues: Array<any>,
  ) {
    let out = '';

    for (const [index, token] of lexingData.entries()) {
      if (index == 0) {
        out += highlightRequestDto.code.substring(0, token.startIndex);
      } else {
        const prevToken = lexingData[index - 1];
        out += highlightRequestDto.code.substring(
          prevToken.endIndex + 1,
          token.startIndex,
        );
      }
      const substring = highlightRequestDto.code.substring(
        token.startIndex,
        token.endIndex + 1,
      );
      const className = HCodes[hCodeValues[index]];

      out += `<span class='${className}'>${substring}</span>`;
    }
    return `${HtmlGeneratorService.prefix}${out}${HtmlGeneratorService.postfix}`;
  }

  // This prefix contains the base html content, with the style definitions
  static prefix = `<!DOCTYPE html>
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
    <pre><code>`;

  // This postfix closes the last few html-tags
  static postfix = `
    </code>
    </pre>
    </html>`;
}
