import { HttpClient, HttpHandler } from '@angular/common/http';
import { ApiService } from './api.service';
import { RouterTestingModule } from '@angular/router/testing';
import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { ChartsModule } from 'ng2-charts';
import { FormsModule } from '@angular/forms';

describe('ApiService', () => {
    beforeEach(() => TestBed.configureTestingModule({
        declarations: [AppComponent],
        imports: [RouterTestingModule, ChartsModule, RouterTestingModule, FormsModule],
        providers: [HttpClient, HttpHandler]
    }));

    it('should be created', () => {
        const service: ApiService = TestBed.get(ApiService);

        expect(service).toBeTruthy();
    });
});
