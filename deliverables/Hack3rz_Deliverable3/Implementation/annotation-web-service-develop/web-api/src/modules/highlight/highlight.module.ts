import { HttpModule } from '@nestjs/axios';
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { HtmlGeneratorService } from 'src/html-generator/html-generator.service';
import configuration from '../../config/configuration';
import { HighlightController } from './highlight.controller';
import { HighlightService } from './highlight.service';

@Module({
  imports: [
    ConfigModule.forRoot({load: [configuration]}),
    HttpModule,
  ],
  controllers: [HighlightController],
  providers: [HighlightService, HtmlGeneratorService],
})
export class HighlightModule {

}