import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  defaultRouter(): string {
    return 'Congrats, you reached the defaultRouter of our API! 🎉';
  }
}
