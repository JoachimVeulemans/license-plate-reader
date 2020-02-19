import { Component } from '@angular/core';
import { ApiService } from './api.service';
import { SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
    selectedFile: File;
    licenses = [];
    id: string;
    url: string;
    busy = false;

    constructor(private apiService: ApiService) {
        this.url = apiService.API_URL;
    }

    upload(): void {
        this.busy = true;
        this.apiService.detect_license(this.selectedFile).subscribe((value) => {
            this.licenses = value.licenses;
            this.id = value.id;
            console.log(value);
            this.busy = false;
        }, (error) => {
            console.log('====================================');
            console.log(error.message);
            console.log('====================================');
        });
    }

    handleFileInput(files: FileList): void {
        this.selectedFile = files[0];

        const reader = new FileReader();

        if (this.selectedFile) {
          reader.readAsDataURL(this.selectedFile);
        }
    }
}
