import { Test } from '@nestjs/testing';
import { HtmlGeneratorService } from '../html-generator/html-generator.service';
import { HighlightModule } from './highlight/highlight.module';
import { HighlightService } from './highlight/highlight.service';

describe('HighlightModule', () => {
  it('should compile the module', async () => {
    const module = await Test.createTestingModule({
      imports: [HighlightModule],
    }).compile();

    expect(module).toBeDefined();
    expect(module.get(HighlightService)).toBeInstanceOf(HighlightService);
    expect(module.get(HtmlGeneratorService)).toBeInstanceOf(
      HtmlGeneratorService,
    );
  });
});
