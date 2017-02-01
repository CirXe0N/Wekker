import {Injectable} from "@angular/core";
import * as moment from "moment";
import Moment = moment.Moment;

@Injectable()
export class DatesService {

  public getTodayObject(): Moment {
    return moment();
  }

  public getDateObject(date: string): Moment {
    return moment(date);
  }

  public convertToYear(date: string): string {
    return moment(date).format('YYYY');
  }

  public convertToShortDate(date: string): string {
    return moment(date).format('MMM D, YYYY');
  }
}
