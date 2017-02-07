import {Component, Input, OnInit} from "@angular/core";
import {CrewMember, CastMember} from "./crew-list.interface";

declare let _: any;

@Component({
  selector: 'crew-list',
  templateUrl: './crew-list.component.html',
  styleUrls: ['./crew-list.component.sass']
})

export class CrewListComponent implements OnInit {
  private selectedTab: string = 'Cast';
  private crewMembersSplit: any[] = [];
  private castMembersSplit: any[] = [];

  @Input() crewMembers: CrewMember[] = [];
  @Input() castMembers: CastMember[] = [];

  ngOnInit(): void {
    if(this.crewMembers.length > 0) {
      let count = Math.ceil(this.crewMembers.length / 2);
      this.crewMembersSplit = _.chunk(this.crewMembers, count);
    }

    if(this.castMembers.length > 0) {
      let count = Math.ceil(this.castMembers.length / 2);
      this.castMembersSplit = _.chunk(this.castMembers, count)
    }
  }
}
