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
    license = '';
    originalUrl = '';
    plateUrl = '';

    constructor(private apiService: ApiService) { }

    upload(): void {
        this.apiService.detect_license(this.selectedFile).subscribe((value) => {
            this.license = value.license;
            this.originalUrl = this.apiService.get_car_url(value.id);
            this.plateUrl = this.apiService.get_plate_url(value.id);
            console.log(value);
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
