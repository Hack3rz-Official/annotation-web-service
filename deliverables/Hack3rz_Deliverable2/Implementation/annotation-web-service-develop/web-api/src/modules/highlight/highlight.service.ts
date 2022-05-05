import { HttpService } from '@nestjs/axios';
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom, Observable } from 'rxjs';
import { HighlightRequestDto } from './dto/highlight-request.dto';
import { HtmlGeneratorService } from 'src/html-generator/html-generator.service';

@Injectable()
export class HighlightService {
  private readonly logger = new Logger(HighlightService.name);

  constructor(
    private config: ConfigService,
    private httpService: HttpService,
    private htmlGeneratorService: HtmlGeneratorService,
  ) {
  }

  async highlight(highlightRequestDto: HighlightRequestDto): Promise<any> {
    // TODO: error handling in case functions return error

    this.logger.debug(`lex.url=${this.config.get('lex.url')}`);

    const lexingRequest: Observable<any> = this.httpService.post(
      this.config.get('lex.url'),
      {
        language: highlightRequestDto.language.toUpperCase(),
        code: highlightRequestDto.code,
      },
    );

    const lexingResponse = await firstValueFrom(lexingRequest)
    const lexingData = lexingResponse.data
    this.logger.log('The lexing function returned', lexingData)

    // generate array with tokenIds from lexingResponse
    const tok_ids = lexingData.map(tok => {
      return tok.tokenId
    })

    this.logger.debug(`predict.url=${this.config.get('predict.url')}`);
    const predictRequest: Observable<any> = this.httpService.post(
      this.config.get('predict.url'),
      {
        lang_name: highlightRequestDto.language,
        tok_ids: tok_ids,
      },
    );
    const predictResponse = await firstValueFrom(predictRequest)
    this.logger.log('The predict function returned', predictResponse.data)

    return this.htmlGeneratorService.buildHtml(highlightRequestDto, lexingData, predictResponse.data.h_code_values)
  }
}