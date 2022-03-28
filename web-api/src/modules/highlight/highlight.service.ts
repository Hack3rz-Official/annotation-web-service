import { HttpService } from '@nestjs/axios';
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom, Observable } from 'rxjs';
import { HighlightRequestDto } from './dto/highlight-request.dto';

@Injectable()
export class HighlightService {
  private readonly logger = new Logger(HighlightService.name);

  constructor(
    private config: ConfigService,
    private httpService: HttpService,
  ) {
  }

  async highlight(highlightRequestDto: HighlightRequestDto): Promise<any> {
    // TODO: Add dev/prod URLs in azure (Function > Settings > Configuration > add all necessary env variables)
    // TODO: error handling in case functions return error

    this.logger.log(highlightRequestDto)

    const lexingRequest: Observable<any> = this.httpService.post(
      this.config.get('lex.url'),
      {
        lang_name: highlightRequestDto.language,
        code: highlightRequestDto.code,
      },
    );
    const lexingData = await firstValueFrom(lexingRequest)
    this.logger.log('The lexing function returned', lexingData.data)

    const predictRequest: Observable<any> = this.httpService.post(
      this.config.get('predict.url'),
      {
        lang_name: highlightRequestDto.language,
        tok_ids: lexingData.data,
      },
    );
    const predictData = await firstValueFrom(predictRequest)
    this.logger.log('The predict function returned', predictData.data)

    return predictData.data
  }
}
