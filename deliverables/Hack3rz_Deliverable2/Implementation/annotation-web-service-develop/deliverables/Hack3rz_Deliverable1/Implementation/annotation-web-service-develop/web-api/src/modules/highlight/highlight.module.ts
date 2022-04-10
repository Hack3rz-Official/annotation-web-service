import { HttpModule } from '@nestjs/axios';
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import configuration from '../../config/configuration';
import { HighlightController } from './highlight.controller';
import { HighlightService } from './highlight.service';

@Module({
  imports: [
    ConfigModule.forRoot({load: [configuration]}),
    HttpModule,
  ],
  controllers: [HighlightController],
  providers: [HighlightService],
})
export class HighlightModule {

}