import { HttpService } from '@nestjs/axios';
import { ConfigService } from '@nestjs/config';
import { Test, TestingModule } from '@nestjs/testing';
import { of } from 'rxjs';
import {
  getMockHCodeValues,
  getMockHighlightRequestDto,
  getMockLexingData,
  getMockResultHtml,
} from '../../../test/mock/test-data';
import { HtmlGeneratorService } from '../../html-generator/html-generator.service';
import { HighlightService } from './highlight.service';

describe('HighlightService', () => {
  let service: HighlightService;
  let httpService: HttpService;
  let htmlGeneratorService: HtmlGeneratorService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        HighlightService,
        ConfigService,
        HtmlGeneratorService,
        {
          provide: HttpService,
          useValue: {
            post: jest.fn((url: string, data: any) => {
              // this is to mock the data from the lexing endpoint
              if (data.language) {
                return of({ data: getMockLexingData() });
              }
              // this is to mock the data from the prediction endpoint
              if (data.tok_ids) {
                return of({ data: { h_code_values: getMockHCodeValues() } });
              }
            }),
          },
        },
      ],
    }).compile();

    service = module.get<HighlightService>(HighlightService);
    httpService = module.get<HttpService>(HttpService);
    htmlGeneratorService =
      module.get<HtmlGeneratorService>(HtmlGeneratorService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  /**
   * Test if the highlight service uses the http service and
   * gets the correct result back from the html generator service
   */
  it('should return highlighted code correctly', async () => {
    const highlightServiceSpy = jest.spyOn(service, 'highlight');
    const httpServiceSpy = jest.spyOn(httpService, 'post');
    const htmlGeneratorServiceSpy = jest.spyOn(
      htmlGeneratorService,
      'buildHtml',
    );

    const highlightedResult = await service.highlight(
      getMockHighlightRequestDto(),
    );

    // verify result is as expected
    expect(highlightedResult).toEqual(getMockResultHtml());
    // verify services are called as expected
    expect(httpServiceSpy).toHaveBeenCalled();
    expect(highlightServiceSpy).toHaveBeenCalledWith(
      getMockHighlightRequestDto(),
    );
    expect(htmlGeneratorServiceSpy).toHaveBeenCalledWith(
      getMockHighlightRequestDto(),
      getMockLexingData(),
      getMockHCodeValues(),
    );
  });
});
