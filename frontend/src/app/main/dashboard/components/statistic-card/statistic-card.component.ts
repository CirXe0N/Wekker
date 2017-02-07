import {Component, Input} from "@angular/core";

@Component({
  selector: 'statistic-card',
  templateUrl: './statistic-card.component.html',
  styleUrls: ['./statistic-card.component.sass']
})

export class StatisticCardComponent {
  @Input() description: string = '--';
  @Input() amount: string = '--';
}
