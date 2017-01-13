import {Pipe , PipeTransform ,Injectable} from "@angular/core";

@Pipe({
  name: 'search'
})

@Injectable()
export class CollectionListSearchPipe implements PipeTransform {

  transform(items: any, value: any): any {
    if(value) {
      return items.filter(item => {
        return item.title.toLowerCase().includes(value.toLowerCase());
      })
    } else {
      return items;
    }
  }
}
