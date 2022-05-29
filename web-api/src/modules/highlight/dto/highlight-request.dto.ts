import { IsEnum, IsNotEmpty, IsString } from 'class-validator';
import { SupportedLanguage } from '../../../constants/supported-languages.enum';

export class HighlightRequestDto {
  @IsNotEmpty()
  @IsString()
  code: string;

  @IsNotEmpty()
  @IsEnum(SupportedLanguage, {
    message: `language is not supported. Supported languages are ${Object.keys(
      SupportedLanguage,
    )
      .map((key) => SupportedLanguage[key])
      .join(', ')}`,
  })
  language: SupportedLanguage;
}
