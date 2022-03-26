import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class AppService {
  constructor(private httpService: HttpService) {}
  
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
    var res = await this.httpService.post(
      'https://hack3rz-functions-java.azurewebsites.net/api/JavaLex',
      { code: code }
    );
    var lexingData = await firstValueFrom(res)
    console.log("The lexing function returned", lexingData.data)
    
    // call predict function
    var res = await this.httpService.post(
      'https://hack3rz-functions-python.azurewebsites.net/api/predict?code=tBcDozZ5IATe/RJtBoa9iIfmJ4SElKT4pZL3KACg0oVmqYMGeHHnMw==',
      {
        lang_name: 'java', // TODO: parametrize
        tok_ids: lexingData.data // use tok_ids received from lexing function
      }
    );
    var predictData = await firstValueFrom(res)
    console.log("The predict function returned", predictData.data)
    
    return predictData.data
  }
}
