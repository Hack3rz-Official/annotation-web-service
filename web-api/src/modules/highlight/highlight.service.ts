import { HttpService } from '@nestjs/axios';
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom, Observable } from 'rxjs';
import { HtmlGeneratorService } from '../../html-generator/html-generator.service';
import { HighlightRequestDto } from './dto/highlight-request.dto';

@Injectable()
export class HighlightService {
  private readonly logger = new Logger(HighlightService.name);

  constructor(
    private config: ConfigService,
    private httpService: HttpService,
    private htmlGeneratorService: HtmlGeneratorService,
  ) {}

  /**
   * This method calls the lexing service and maps the returned tokens,
   * it then uses the tokens to make the prediction service call to predict the
   * h code values based on the tokens.
   * Additionally, the different steps are timed for debugging purposes.
   *  @param {HighlightRequestDto} highlightRequestDto The request dto containing the language and the code to be highlighted.
   */
  async highlight(highlightRequestDto: HighlightRequestDto): Promise<any> {
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

    const lexingResponse = await firstValueFrom(lexingRequest);
    this.logger.debug(
      `Lexing request took: ${new Date().getTime() - start_time} ms`,
    );
    const lexingData = lexingResponse.data;

    // generate array with tokenIds from lexingResponse
    const tok_ids = lexingData.map((tok) => {
      return tok.tokenId;
    });

    this.logger.debug(`predict.url=${this.config.get('predict.url')}`);
    start_time = new Date().getTime();
    const predictRequest: Observable<any> = this.httpService.post(
      this.config.get('predict.url'),
      {
        lang_name: highlightRequestDto.language,
        tok_ids: tok_ids,
      },
    );
    const predictResponse = await firstValueFrom(predictRequest);
    this.logger.debug(
      `Predict request took: ${new Date().getTime() - start_time} ms`,
    );
    this.logger.debug(
      `Total request took: ${new Date().getTime() - request_time} ms`,
    );

    return this.htmlGeneratorService.buildHtml(
      highlightRequestDto,
      lexingData,
      predictResponse.data.h_code_values,
    );
  }
}
