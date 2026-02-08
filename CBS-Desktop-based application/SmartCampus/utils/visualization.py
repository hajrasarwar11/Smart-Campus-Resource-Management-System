"""
Data Visualization Module using Matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
import os


class MatplotlibCanvas(QWidget):
    """Canvas for displaying matplotlib figures in PyQt5"""
    
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_booking_status_pie(self, status_counts):
        """Plot booking status as pie chart"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            labels = list(status_counts.keys())
            sizes = list(status_counts.values())
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)], startangle=90)
            ax.set_title('Booking Status Distribution', fontsize=14, fontweight='bold')
            
            self.canvas.draw()
        except Exception as e:
            print(f"Pie chart error: {e}")
    
    def plot_room_utilization(self, room_data):
        """Plot room utilization as bar chart"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            rooms = list(room_data.keys())
            utilization = list(room_data.values())
            
            bars = ax.bar(rooms, utilization, color='#66b3ff', edgecolor='black')
            ax.set_ylabel('Utilization (%)', fontsize=12)
            ax.set_xlabel('Classrooms', fontsize=12)
            ax.set_title('Room Utilization Rate', fontsize=14, fontweight='bold')
            ax.set_ylim(0, 100)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}%', ha='center', va='bottom', fontsize=9)
            
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Bar chart error: {e}")
    
    def plot_bookings_by_day(self, day_data):
        """Plot bookings by day as line chart"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            days = list(day_data.keys())
            counts = list(day_data.values())
            
            ax.plot(days, counts, marker='o', linewidth=2, markersize=8, color='#66b3ff')
            ax.fill_between(range(len(days)), counts, alpha=0.3, color='#66b3ff')
            ax.set_ylabel('Number of Bookings', fontsize=12)
            ax.set_xlabel('Day of Week', fontsize=12)
            ax.set_title('Bookings by Day', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Set integer ticks
            ax.set_xticks(range(len(days)))
            ax.set_xticklabels(days, rotation=45)
            
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Line chart error: {e}")
    
    def plot_teacher_workload(self, teacher_data):
        """Plot teacher workload as horizontal bar chart"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            teachers = list(teacher_data.keys())
            workload = list(teacher_data.values())
            
            bars = ax.barh(teachers, workload, color='#99ff99', edgecolor='black')
            ax.set_xlabel('Number of Classes', fontsize=12)
            ax.set_title('Teacher Workload Distribution', fontsize=14, fontweight='bold')
            
            # Add value labels on bars
            for bar in bars:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f'{int(width)}', ha='left', va='center', fontsize=9)
            
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Horizontal bar chart error: {e}")


class VisualizationHelper:
    """Helper class to prepare data for visualization"""
    
    @staticmethod
    def get_booking_status_data(bookings):
        """Prepare booking status data from list of bookings"""
        status_map = {0: "Cancelled", 1: "Approved", 2: "Pending", 3: "Rejected"}
        status_counts = {status: 0 for status in status_map.values()}
        
        for booking in bookings:
            status = status_map.get(booking.status, "Unknown")
            status_counts[status] += 1
        
        return {k: v for k, v in status_counts.items() if v > 0}
    
    @staticmethod
    def get_room_utilization(classrooms, bookings):
        """Calculate room utilization percentage"""
        room_usage = {}
        
        for classroom in classrooms:
            total_time_slots = 40  # Assuming 8 hours per day, 5 days = 40 slots
            used_slots = len([b for b in bookings if b.classroom_id == classroom.id])
            utilization = min(100, (used_slots / total_time_slots) * 100)
            room_usage[classroom.room_number] = utilization
        
        return room_usage
    
    @staticmethod
    def get_bookings_by_day(bookings):
        """Group bookings by day of week"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_counts = {day: 0 for day in days}
        
        # For now, distribute bookings randomly across days
        # In production, you'd use actual booking dates
        if bookings:
            per_day = len(bookings) // 5
            for i, day in enumerate(days):
                day_counts[day] = per_day + (1 if i < len(bookings) % 5 else 0)
        
        return day_counts
    
    @staticmethod
    def get_teacher_workload(teachers, schedules):
        """Calculate teacher workload (number of classes)"""
        workload = {}
        
        for teacher in teachers:
            class_count = len([s for s in schedules if s.teacher_id == teacher.id])
            if class_count > 0:
                workload[teacher.fullname[:20]] = class_count  # Truncate long names
        
        return dict(sorted(workload.items(), key=lambda x: x[1], reverse=True)[:10])  # Top 10
