import { ArgumentMetadata, ValidationPipe } from '@nestjs/common';
import { HighlightRequestDto } from './highlight-request.dto';

describe('HighlightRequestDto', () => {
  it('should be defined', () => {
    expect(new HighlightRequestDto()).toBeDefined();
  });

  it('should validate the HighlightRequestDto definition', async () => {
    const target: ValidationPipe = new ValidationPipe({
      transform: true,
      whitelist: true,
    });
    const metadata: ArgumentMetadata = {
      type: 'body',
      metatype: HighlightRequestDto,
      data: '{}',
    };
    const expected: string[] = [
      'code must be a string',
      'code should not be empty',
      'language is not supported. Supported languages are java, kotlin, python3',
      'language should not be empty',
    ];
    await target.transform(<HighlightRequestDto>{}, metadata).catch((err) => {
      expect(err.getResponse().message).toEqual(expected);
    });
  });
});
