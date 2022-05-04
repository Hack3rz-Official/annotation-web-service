import { HttpService } from '@nestjs/axios';
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom, Observable } from 'rxjs';
import { HighlightRequestDto } from './dto/highlight-request.dto';
import { HtmlGeneratorService } from 'src/html-generator/html-generator.service';

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
    // TODO: error handling in case functions return error

    this.logger.debug(`lex.url=${this.config.get('lex.url')}`);

    let start_time = new Date().getTime();
    const request_time = new Date().getTime();

    const lexingRequest: Observable<any> = this.httpService.post(
      this.config.get('lex.url'),
      {
        language: highlightRequestDto.language.toUpperCase(),
        code: highlightRequestDto.code,
      },
    );

    const lexingResponse = await firstValueFrom(lexingRequest)
    this.logger.debug(
      `Lexing request took: ${new Date().getTime() - start_time} ms`,
    );
    const lexingData = lexingResponse.data
    //this.logger.debug('The lexing function returned', lexingData)

    // generate array with tokenIds from lexingResponse
    const tok_ids = lexingData.map(tok => {
      return tok.tokenId
    })

    this.logger.debug(`predict.url=${this.config.get('predict.url')}`);
    start_time = new Date().getTime();
    const predictRequest: Observable<any> = this.httpService.post(
      this.config.get('predict.url'),
      {
        lang_name: highlightRequestDto.language,
        tok_ids: tok_ids,
      },
    );
    const predictResponse = await firstValueFrom(predictRequest)
    this.logger.debug(
      `Predict request took: ${new Date().getTime() - start_time} ms`,
    );
    //this.logger.debug('The predict function returned', predictResponse.data)
    this.logger.debug(
      `Total request took: ${new Date().getTime() - request_time} ms`,
    );
    return this.htmlGeneratorService.buildHtml(highlightRequestDto, lexingData, predictResponse.data.h_code_values)
  }
}