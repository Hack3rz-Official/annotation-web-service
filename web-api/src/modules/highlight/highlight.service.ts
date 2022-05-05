import { HttpService } from '@nestjs/axios';
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom, Observable } from 'rxjs';
import { HighlightRequestDto } from './dto/highlight-request.dto';
import { HtmlGeneratorService } from 'src/html-generator/html-generator.service';
import { v4 as uuidv4 } from 'uuid';


@Injectable()
export class HighlightService {
  constructor(
    private config: ConfigService,
    private httpService: HttpService,
    private htmlGeneratorService: HtmlGeneratorService,
    private readonly logger: Logger
  ) {
  }

  async highlight(highlightRequestDto: HighlightRequestDto): Promise<any> {

    const times = {
      'req_id': uuidv4(),
      'req_in': new Date().getTime(),
      'req_lexed': 0,
      'req_predicted': 0,
      'req_out': 0,
    }

    const request_time = new Date().getTime();

    const lexingRequest: Observable<any> = this.httpService.post(
      this.config.get('lex.url'),
      {
        language: highlightRequestDto.language.toUpperCase(),
        code: highlightRequestDto.code,
      },
    );

    const lexingResponse = await firstValueFrom(lexingRequest)
    // this.logger.debug(
    //   `Lexing request took: ${new Date().getTime() - request_time} ms`,
    // );
    times['req_lexed'] = new Date().getTime()
    const lexingData = lexingResponse.data
    //this.logger.debug('The lexing function returned', lexingData)

    // generate array with tokenIds from lexingResponse
    const tok_ids = lexingData.map(tok => {
      return tok.tokenId
    })

    // start_time = new Date().getTime();
    const predictRequest: Observable<any> = this.httpService.post(
      this.config.get('predict.url'),
      {
        lang_name: highlightRequestDto.language,
        tok_ids: tok_ids,
      },
    );
    const predictResponse = await firstValueFrom(predictRequest)
    // this.logger.debug(
    //   `Predict request took: ${new Date().getTime() - start_time} ms`,
    // );
    times['req_predicted'] = new Date().getTime()
    // this.logger.debug(
    //   `Total request took: ${new Date().getTime() - request_time} ms`,
    // );
    const html = this.htmlGeneratorService.buildHtml(highlightRequestDto, lexingData, predictResponse.data.h_code_values)
    times['req_out'] = new Date().getTime()

    let lexTime = formatMsAsS(times['req_lexed'] - times['req_in'])
    let predictTime = formatMsAsS(times['req_predicted'] - times['req_lexed'])
    let htmlTime = formatMsAsS(times['req_out'] - times['req_predicted'])
    let totalTime = formatMsAsS(times['req_out'] - times['req_in'])
    this.logger.debug(`req ${times['req_id']}: start=${times['req_in']} lex=${lexTime} predict=${predictTime} html=${htmlTime} total=${totalTime} end=${times['req_out']}`)
    return html
  }
}

function formatMsAsS(ms) {
  return (ms / 1000).toFixed(3)
}

// docker exec -it web-api /bin/sh
// cat log/debug/debug.log