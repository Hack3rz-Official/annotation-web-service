import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { HighlightModule } from './modules/highlight/highlight.module';

@Module({
  imports: [HighlightModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {
}
