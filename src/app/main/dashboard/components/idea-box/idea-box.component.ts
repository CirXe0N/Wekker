import {Component} from "@angular/core";
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {WekkerAPIService} from "../../../../../services/wekker-api/wekker-api.service";
import {Feedback} from "./idea-box.interface";

@Component({
  selector: 'idea-box',
  templateUrl: './idea-box.component.html',
  styleUrls: ['./idea-box.component.sass']
})

export class IdeaBoxComponent {
  private form: FormGroup;
  private isRequesting: boolean = false;
  private isSuccessfulRequest: boolean = false;

  constructor(private wekker: WekkerAPIService) {}

  ngOnInit(): void {
    this.form = new FormGroup({
      feedback_type: new FormControl('Idea/Suggestion'),
      message: new FormControl('', Validators.required),
    });
  }

  private doFeedbackRequest({value, valid}: {value: Feedback, valid: boolean}): void {
    this.isRequesting = true;
    if(valid) {
      this.wekker.doPostRequest('/feedback/', value)
        .subscribe(
          res => {
            this.form.reset({feedback_type: 'Idea/Suggestion', message: ''});
            this.isRequesting = false;
            this.isSuccessfulRequest = true;
          },
          err => {
            this.isRequesting = false;
          })
    } else {
      this.isRequesting = false;
    }
  }
}
