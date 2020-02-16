import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private _apiURL = environment.backend_url;
    private optionsWithJSON = { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };

    constructor(private http: HttpClient) { }

    detect_license(image: File): Observable<any> {
        const url = `${this._apiURL}/upload`;
        const uploadData = new FormData();
        uploadData.append('file', image, 'file');
        return this.http.post<any>(url, uploadData);
    }

    get_car_url(id: string): string {
        return `${this._apiURL}/car?id=${id}`;
    }

    get_plate_url(id: string): string {
        return `${this._apiURL}/plate?id=${id}`;
    }
}
