import {Injectable} from "@angular/core";

@Injectable()
export class SettingsService {
  public getEnvVariable(value: string): string {
    let hostname = window.location.hostname;
    let data = {};
    switch (hostname) {
      case 'localhost':
        data = {
          API_ENDPOINT: 'http://localhost:8000'
        };
        break;
      default:
        data = {
          API_ENDPOINT: window.location.protocol + '//' + window.location.host
        };
    }
    return data[value];
  }
}
