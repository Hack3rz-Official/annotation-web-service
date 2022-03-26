import { SupportedLanguage } from '../constants/supported-languages.enum';

export class HighlightRequestDto {
  code: string;
  language: SupportedLanguage
}