import { Body, Controller, Get, HttpCode, Post } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  /*
  In here we can create new routes as needed. check the nest.js documentation for details.
  */

  @Get()
  defaultRouter(): string {
    return this.appService.defaultRouter();
  }

  @Post('/highlight')
  @HttpCode(200)
  highlight(@Body() code: string): Promise<any> {
    return this.appService.highlight(code);
  }
}