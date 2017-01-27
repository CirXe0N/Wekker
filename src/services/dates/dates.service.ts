import {Injectable} from "@angular/core";
import * as moment from "moment";

@Injectable()
export class DatesService {

  public convertToYear(date: string): string {
    return moment(date).format('YYYY');
  }

  public convertToShortDate(date: string): string {
    return moment(date).format('MMM D, YYYY');
  }
}
