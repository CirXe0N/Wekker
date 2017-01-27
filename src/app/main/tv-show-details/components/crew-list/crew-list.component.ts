import {Component, Input} from "@angular/core";
import {CrewMember, CastMember} from "../../tv-show-details.interface";

@Component({
  selector: 'crew-list',
  templateUrl: './crew-list.component.html',
  styleUrls: ['./crew-list.component.sass']
})

export class CrewListComponent {
  @Input() crewMembers: CrewMember[] = [];
  @Input() castMembers: CastMember[] = [];
}
