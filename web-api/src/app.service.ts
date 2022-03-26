import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class AppService {
  constructor(
    private config: ConfigService,
    private httpService: HttpService
  ) {}

  defaultRouter(): string {
    return 'Congrats, you reached the defaultRouter of our API! 🎉';
  }

  async highlight(code): Promise<any> {
    // TODO: find way to hide function URLs in some secret / vault. we do not want them to be exposed in source code
    // TODO: error handling in case functions return error
    // TODO: leverage DTO (https://docs.nestjs.com/controllers#request-payloads) for payload
    // TODO: "typescript-ify" code
    // TODO: additional payload parameter for lang_name (java, python, kotlin) which gets passed to functions
    // TODO: highlight controller and service could be moved to seperate files

    console.log(code)

    // call lexing function
    const lexingResponse = await this.httpService.post(
      this.config.get('lex.url'),
      { code: code }
    );
    const lexingData = await firstValueFrom(lexingResponse)
    console.log("The lexing function returned", lexingData.data)

    // call predict function
    const predictResponse = await this.httpService.post(
     this.config.get('predict.url'),
     {
        lang_name: 'java', // TODO: parametrize
        tok_ids: lexingData.data // use tok_ids received from lexing function
      }
    );
    const predictData = await firstValueFrom(predictResponse)
    console.log("The predict function returned", predictData.data)

    return predictData.data
  }
}
