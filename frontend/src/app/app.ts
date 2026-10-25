
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  selectedPage = 'Dashboard';

  menuItems = [
    'Dashboard',
    'Movement Analysis',
    'Prediction History',
    'Dataset Insights',
    'About Project'
  ];

  selectPage(page: string): void {
    this.selectedPage = page;
  }
}
