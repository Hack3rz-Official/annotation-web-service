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
    console.log(code)

    // call lexing function
    /* 
    var res = await this.httpService.post(
      'ENTER_LEXING_FUNCTION_URL_HERE',
      {code: code}
    );
    var lexingData = await firstValueFrom(res)
    console.log("The lexing function returned", lexingData.data)
    */
    

    var res = await this.httpService.post(
      'https://hack3rz-functions-python.azurewebsites.net/api/predict?code=tBcDozZ5IATe/RJtBoa9iIfmJ4SElKT4pZL3KACg0oVmqYMGeHHnMw==',
      {
        lang_name: 'java', // TODO: parametrize
        tok_ids: [22, 4, 33, 77, 8] // TODO: replace with output from lexing function
      }
    );
    var predictData = await firstValueFrom(res)
    console.log("The predict function returned", predictData.data)
    
    return predictData.data
  }
}
