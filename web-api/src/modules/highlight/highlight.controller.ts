import { Body, Controller, HttpCode, Post } from '@nestjs/common';
import { HighlightRequestDto } from './dto/highlight-request.dto';
import { HighlightService } from './highlight.service';

@Controller()
export class HighlightController {
  constructor(private highlightService: HighlightService) {}

  @Post('/highlight')
  @HttpCode(200)
  highlight(@Body() highlightRequestDto: HighlightRequestDto): Promise<any> {
    return this.highlightService.highlight(highlightRequestDto);
  }
}
