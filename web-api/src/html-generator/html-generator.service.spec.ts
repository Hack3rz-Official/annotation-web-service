import { Test, TestingModule } from '@nestjs/testing';
import {
  getMockHCodeValues,
  getMockHighlightRequestDto,
  getMockLexingData,
  getMockResultHtml,
} from '../../test/mock/test-data';
import { HtmlGeneratorService } from './html-generator.service';

describe('HtmlGeneratorService', () => {
  let service: HtmlGeneratorService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [HtmlGeneratorService],
    }).compile();

    service = module.get<HtmlGeneratorService>(HtmlGeneratorService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  /**
   * Test if the html returned from HtmlGeneratorService
   * contains the expected string based on the lexing tokens and hCodeValues
   */
  it('should return correct html', () => {
    const highlightRequestDto = getMockHighlightRequestDto();

    expect(
      service.buildHtml(
        highlightRequestDto,
        getMockLexingData(),
        getMockHCodeValues(),
      ),
    ).toBe(getMockResultHtml());
  });
});
