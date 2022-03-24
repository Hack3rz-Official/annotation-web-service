import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';

@Injectable()
export class AppService {
  constructor(private httpService: HttpService) {}
  
  defaultRouter(): string {
    return 'Congrats, you reached the defaultRouter of our API! 🎉 Here will nothing happen, but at least you know that communication works :)';
  }

  async highlight(code): Promise<any> {
    console.log(code)
    return 'here we do syntax highlighting.';
  }
}
