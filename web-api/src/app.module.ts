import { Module } from '@nestjs/common';
import { HtmlGeneratorService } from './html-generator/html-generator.service';
import { HighlightModule } from './modules/highlight/highlight.module';

@Module({
  imports: [HighlightModule],
  controllers: [],
  providers: [HtmlGeneratorService],
})
export class AppModule {}
