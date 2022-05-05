import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { HighlightModule } from './modules/highlight/highlight.module';
import { HtmlGeneratorService } from './html-generator/html-generator.service';

@Module({
  imports: [HighlightModule],
  controllers: [AppController],
  providers: [AppService, HtmlGeneratorService],
})
export class AppModule {}
