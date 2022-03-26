import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom } from 'rxjs';
import { HighlightRequestDto } from './dto/highlight-request.dto';

@Injectable()
export class AppService {
  constructor(
    private config: ConfigService,
    private httpService: HttpService
  ) {}

  defaultRouter(): string {
    return 'Congrats, you reached the defaultRouter of our API! 🎉';
  }

  async highlight(highlightRequestDto: HighlightRequestDto): Promise<any> {
    // TODO: Add dev/prod URLs in azure (Function > Settings > Configuration > add all necessary env variables)
    // TODO: Refactor await on non-promise (Observable)
    // TODO: highlight controller and service could be moved to seperate files
    // TODO: error handling in case functions return error

    console.log(highlightRequestDto)

    // call lexing function
    const lexingResponse = await this.httpService.post(
      this.config.get('lex.url'),
      { code: highlightRequestDto.code }
    );
    const lexingData = await firstValueFrom(lexingResponse)
    console.log("The lexing function returned", lexingData.data)

    // call predict function
    const predictResponse = await this.httpService.post(
     this.config.get('predict.url'),
     {
        lang_name: highlightRequestDto.language,
        tok_ids: lexingData.data // use tok_ids received from lexing function
      }
    );
    const predictData = await firstValueFrom(predictResponse)
    console.log("The predict function returned", predictData.data)

    return predictData.data
  }
}
