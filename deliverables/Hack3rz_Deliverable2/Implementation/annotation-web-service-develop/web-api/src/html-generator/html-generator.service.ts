import { Injectable } from '@nestjs/common';
import { HighlightRequestDto } from 'src/modules/highlight/dto/highlight-request.dto';
import { HCodes } from 'src/constants/hcodes.enum'; 

@Injectable()
export class HtmlGeneratorService {

    buildHtml(highlightRequestDto: HighlightRequestDto, lexingData: Array<any>, hCodeValues: Array<any>) {

        // console.log(highlightRequestDto)
        // console.log(lexingData)
        // console.log(hCodeValues)

        let out = ""
        
        for (const [index, token] of lexingData.entries()) {
            if (index == 0) {
                out += highlightRequestDto.code.substring(0, token.startIndex)
            } else {
                let prevToken = lexingData[index - 1]
                out += highlightRequestDto.code.substring(prevToken.endIndex + 1, token.startIndex)
            }
            let substring = highlightRequestDto.code.substring(token.startIndex, token.endIndex + 1)
            let className = HCodes[hCodeValues[index]]

            out += `<span class='${className}'>${substring}</span>`
        }
        return `${HtmlGeneratorService.prefix}${out}${HtmlGeneratorService.postfix}`
    }

    static prefix = `
    <!DOCTYPE html>
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
    <pre><code>`
    
    static postfix = `
    </pre>
    </code>
    </html>
    `
}
