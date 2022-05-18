import { ArgumentMetadata, ValidationPipe } from '@nestjs/common';
import { HighlightRequestDto } from './highlight-request.dto';

describe('HighlightRequestDto', () => {
  it('should be defined', () => {
    expect(new HighlightRequestDto()).toBeDefined();
  });

  /**
   * This test is used to make sure that the different validation requirements
   * specified for the highlight request dto are met (i.e., error messages in `expected`).
   */
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
    // These error messages should appear when trying to use a completely invalid dto.
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
