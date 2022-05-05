import { Test, TestingModule } from '@nestjs/testing';
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
});
