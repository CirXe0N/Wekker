import {Injectable} from "@angular/core";
import {Http, Headers} from "@angular/http";
import {SettingsService} from "../settings/settings.service";
import {Observable} from "rxjs";
import {Router} from "@angular/router";

@Injectable()
export class WekkerAPIService {
  private API_SERVER_URL: string;

  constructor(private http: Http, private router: Router, private settings: SettingsService) {
    this.API_SERVER_URL = settings.getEnvVariable('API_ENDPOINT') + '/api/v1';
  }

  public doGetRequest(uri: string, isPublicRequest: boolean = false) {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');

    if(!isPublicRequest) {
      headers.append('Authorization', 'Token ' + localStorage.getItem('WekkerAccessToken'));
    }

    return this.http.get(this.API_SERVER_URL + uri, {headers: headers})
      .map(res => res.json())
      .catch(err => this.handleError(err));
  }

  public doPostRequest(uri: string, body: any, isPublicRequest: boolean = false) {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');

    if(!isPublicRequest) {
      headers.append('Authorization', 'Token ' + localStorage.getItem('WekkerAccessToken'));
    }

    return this.http.post(this.API_SERVER_URL + uri, JSON.stringify(body), {headers: headers})
      .map(res => res.json())
      .catch(err => this.handleError(err));
  }

  public doPutRequest(uri: string, body: any, isPublicRequest: boolean = false) {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');

    if(!isPublicRequest) {
      headers.append('Authorization', 'Token ' + localStorage.getItem('WekkerAccessToken'));
    }

    return this.http.put(this.API_SERVER_URL + uri, JSON.stringify(body), {headers: headers})
      .map(res => res.json())
      .catch(err => this.handleError(err));
  }

  private handleError(error: any): Observable<any> {
    if(error.status == 401) {
      localStorage.removeItem('WekkerAccessToken');
      this.router.navigate(['/home']);
    }
    return Observable.throw(error.json() || 'Server Error')
  }
}
