import {Component, OnInit, trigger, transition, style, animate} from '@angular/core';

@Component({
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.sass'],
  animations: [
    trigger("dynamicText", [
      transition("* => *", [
        style({ opacity: 0 }),
        animate(1000)
      ]),
    ])]

})

export class LandingPageComponent implements OnInit {
  private switchToLogin: boolean = false;
  private switchToForgetPassword: boolean = false;
  private informationMessage: string;
  private informationMessageIndex: number = 0;
  private informationMessages: string[] = [
    'the release of a TV show episode or movie.',
    'the episode discussions with friends and family.',
    'the TV show recommendation from your friends and family.'
  ];

  constructor() {}

  ngOnInit() {
    this.loopInformationMessages();
  }

  private loopInformationMessages() {
    if(this.informationMessages.length > 0 ) {
      if(this.informationMessageIndex == this.informationMessages.length) {
        this.informationMessageIndex = 0;
      }
      this.informationMessage = this.informationMessages[this.informationMessageIndex];
      this.informationMessageIndex++;
    }

    setTimeout(() => {
      this.loopInformationMessages();
    }, 3000);
  }
}

