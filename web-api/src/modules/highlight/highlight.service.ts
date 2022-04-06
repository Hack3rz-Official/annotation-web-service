import { HttpService } from '@nestjs/axios';
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { throws } from 'assert';
import { firstValueFrom, Observable } from 'rxjs';
import { HighlightRequestDto } from './dto/highlight-request.dto';
import { HtmlGeneratorService } from 'src/html-generator/html-generator.service';

@Injectable()
export class HighlightService {
  private readonly logger = new Logger(HighlightService.name);

  constructor(
    private config: ConfigService,
    private httpService: HttpService,
    private htmlGeneratorService: HtmlGeneratorService,
  ) {
  }

  async highlight(highlightRequestDto: HighlightRequestDto): Promise<any> {
    // TODO: error handling in case functions return error

    this.logger.log(highlightRequestDto)

    // TODO: make this API call work (inside docker)
    // const lexingRequest: Observable<any> = this.httpService.post(
    //   'http://127.0.0.1:8080/api/annotate',
    //   {
    //     lang_name: highlightRequestDto.language,
    //     code: highlightRequestDto.code,
    //   },
    // );

    // const lexingResponse = await firstValueFrom(lexingRequest)
    // const lexingData = lexingResponse.data
    // this.logger.log('The lexing function returned', lexingData)

    // hardcoded for development
    const lexingData = [
      { startIndex: 0, endIndex: 5, tokenId: 35 }, 
      { startIndex: 7, endIndex: 12, tokenId: 38 }, 
      { startIndex: 14, endIndex: 17, tokenId: 48 }, 
      { startIndex: 19, endIndex: 22, tokenId: 102 }, 
      { startIndex: 23, endIndex: 23, tokenId: 57 }, 
      { startIndex: 24, endIndex: 29, tokenId: 102 }, 
      { startIndex: 30, endIndex: 30, tokenId: 61 }, 
      { startIndex: 31, endIndex: 31, tokenId: 62 }, 
      { startIndex: 33, endIndex: 36, tokenId: 102 }, 
      { startIndex: 37, endIndex: 37, tokenId: 58 }, 
      { startIndex: 39, endIndex: 39, tokenId: 59 }, 
      { startIndex: 40, endIndex: 40, tokenId: 60 }
    ]

    // generate array with tokenIds from lexingResponse
    const tok_ids = lexingData.map(tok => {
      return tok.tokenId
    })

    // TODO: make this API call work (inside docker)
    const predictRequest: Observable<any> = this.httpService.post(
      "http://127.0.0.1:5000/predict",
      {
        lang_name: highlightRequestDto.language,
        tok_ids: tok_ids,
      },
    );
    const predictResponse = await firstValueFrom(predictRequest)
    this.logger.log('The predict function returned', predictResponse.data)

    return this.htmlGeneratorService.buildHtml(highlightRequestDto, lexingData, predictResponse.data.h_code_values)
  }
}