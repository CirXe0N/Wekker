import {Component, OnInit} from "@angular/core";
import {User} from "../../../services/utilities/utilities.interface";
import {UtilitiesService} from "../../../services/utilities/utilities.service";
import {WekkerAPIService} from "../../../services/wekker-api/wekker-api.service";
import {FormGroup, FormControl, Validators, FormBuilder} from "@angular/forms";

@Component({
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.sass']
})

export class UserProfileComponent implements OnInit {
  private profileForm: FormGroup;
  private passwordForm: FormGroup;
  private user: User;
  private isLoading: boolean = false;
  private selectedTab: string = 'Profile';
  private selectedProfilePhoto: string;
  private selectedProfilePhotoName: string;
  private isRequestingProfile: boolean = false;
  private isRequestingPassword: boolean = false;
  private isSuccessfulProfileRequest: boolean = false;
  private isSuccessfulPasswordRequest: boolean = false;
  private requestError: any[] = [];

  constructor(private wekker: WekkerAPIService, private utilities: UtilitiesService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.getUser();

    this.profileForm = new FormGroup({
      first_name: new FormControl('', Validators.required),
      last_name: new FormControl('', Validators.required)
    });

    this.passwordForm = this.fb.group({
      old_password: ['', Validators.required],
      password: ['', Validators.compose([Validators.required, Validators.minLength(5)])],
      repeatPassword: ['', Validators.required]
    }, {validator: this.areEqualPasswords});
  }

  private getUser(): void {
    this.isLoading = true;
    this.utilities.getUser()
      .subscribe(res => {
        this.user = res;
        this.isLoading = false;
      });
  }

  private selectTab(tab: string): void {
    this.selectedTab = tab;
    this.resetButtons();
  }

  private selectProfilePhoto(file: File) {
    let reader = new FileReader();
    reader.onload = () =>  {
      this.selectedProfilePhoto = reader.result;
      this.selectedProfilePhotoName = file.name;
    };
    reader.readAsDataURL(file);
  }

  private doSaveProfileRequest({value, valid}: {value: User, valid: boolean}): void {
    if(valid) {
      this.isRequestingProfile = true;
      value.photo = this.selectedProfilePhoto;
      value.photo_name = this.selectedProfilePhotoName;
      this.wekker.doPutRequest('/users/', value)
        .subscribe(
          res => {
            this.utilities.setUser(res);
            this.isSuccessfulProfileRequest = true;
            this.isRequestingProfile = false;
          },
          err => {
            this.isRequestingProfile = false;
          }
        )
    }
  }

  private doSavePasswordRequest({value, valid}: {value: User, valid: boolean}): void {
    if(valid) {
      this.isRequestingPassword = true;
      this.wekker.doPutRequest('/users/', value)
        .subscribe(
          res => {
            this.passwordForm.reset();
            this.isSuccessfulPasswordRequest = true;
            this.isRequestingPassword = false;
          },
          err => {
            this.requestError = err;
            this.isRequestingPassword = false;
          }
        )
    }
  }

  private resetButtons(): void {
    this.isSuccessfulProfileRequest = false;
    this.isSuccessfulPasswordRequest = false;
    this.passwordForm.reset();
  }

  private resetRequestError(): void {
    this.requestError = [];
  }

  private areEqualPasswords(group: FormGroup) {
    let password = group.get('password').value;
    let repeatPassword = group.get('repeatPassword').value;
    if(password == repeatPassword) {
      return null
    }

    return {
      areNotEqualPasswords : true
    };
  }
}
