"""
Reports Module
"""

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from models.booking import Booking
from models.schedule import Schedule
from models.classroom import Classroom
from database.db_setup import DatabaseManager

class ReportGenerator:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_booking_stats(self):
        """Get booking statistics"""
        all_bookings = Booking.get_all_bookings()
        
        stats = {
            'total': len(all_bookings),
            'approved': len([b for b in all_bookings if b.status == 1]),
            'pending': len([b for b in all_bookings if b.status == 2]),
            'rejected': len([b for b in all_bookings if b.status == 3]),
            'cancelled': len([b for b in all_bookings if b.status == 0]),
        }
        
        return stats
    
    def get_resource_usage(self):
        """Get resource usage statistics"""
        classrooms = Classroom.get_all_classrooms()
        
        usage_data = {}
        for classroom in classrooms:
            bookings = self.db.execute_query(
                'SELECT COUNT(*) FROM bookings WHERE classroom_id = ? AND status = 1',
                (classroom.id,)
            )
            usage_data[classroom.room_number] = bookings[0][0] if bookings else 0
        
        return usage_data
    
    def get_peak_hours(self):
        """Get peak booking hours"""
        query = '''
            SELECT start_time, COUNT(*) as count 
            FROM bookings 
            WHERE status = 1
            GROUP BY start_time
            ORDER BY count DESC
        '''
        results = self.db.execute_query(query)
        
        peak_hours = {}
        if results:
            for time, count in results:
                peak_hours[time] = count
        
        return peak_hours
    
    def get_underutilized_rooms(self, threshold=2):
        """Get underutilized classrooms"""
        classrooms = Classroom.get_all_classrooms()
        underutilized = []
        
        for classroom in classrooms:
            bookings = self.db.execute_query(
                'SELECT COUNT(*) FROM bookings WHERE classroom_id = ? AND status = 1',
                (classroom.id,)
            )
            count = bookings[0][0] if bookings else 0
            
            if count <= threshold:
                underutilized.append({
                    'room': classroom.room_number,
                    'type': classroom.room_type,
                    'bookings': count
                })
        
        return underutilized
    
    def export_report_to_text(self, filename='resource_report.txt'):
        """Export report to text file"""
        with open(filename, 'w') as f:
            f.write("Smart Campus Resource Management Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Booking Stats
            stats = self.get_booking_stats()
            f.write("BOOKING STATISTICS\n")
            f.write("-" * 60 + "\n")
            f.write(f"Total Bookings: {stats['total']}\n")
            f.write(f"Approved: {stats['approved']}\n")
            f.write(f"Pending: {stats['pending']}\n")
            f.write(f"Rejected: {stats['rejected']}\n")
            f.write(f"Cancelled: {stats['cancelled']}\n\n")
            
            # Resource Usage
            f.write("RESOURCE USAGE\n")
            f.write("-" * 60 + "\n")
            usage = self.get_resource_usage()
            for room, count in usage.items():
                f.write(f"{room}: {count} bookings\n")
            
            f.write("\n")
            
            # Peak Hours
            f.write("PEAK HOURS\n")
            f.write("-" * 60 + "\n")
            peak_hours = self.get_peak_hours()
            for time, count in sorted(peak_hours.items(), key=lambda x: x[1], reverse=True)[:5]:
                f.write(f"{time}: {count} bookings\n")
            
            f.write("\n")
            
            # Underutilized Rooms
            f.write("UNDERUTILIZED ROOMS\n")
            f.write("-" * 60 + "\n")
            underutilized = self.get_underutilized_rooms()
            for room_info in underutilized:
                f.write(f"{room_info['room']} ({room_info['type']}): {room_info['bookings']} bookings\n")
        
        return filename


class ReportChartWidget(QWidget):
    """Widget for displaying report charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.generator = ReportGenerator()
        self.init_ui()
    
    def init_ui(self):
        """Initialize chart widget"""
        layout = QVBoxLayout(self)
        
        title = QLabel("Resource Usage Report")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.plot_booking_stats()
    
    def plot_booking_stats(self):
        """Plot booking statistics"""
        stats = self.generator.get_booking_stats()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        labels = list(stats.keys())
        sizes = list(stats.values())
        colors = ['#0EA5E9', '#059669', '#F59E0B', '#DC2626', '#6B7280']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.set_title('Booking Status Distribution')
        
        self.canvas.draw()
    
    def plot_resource_usage(self):
        """Plot resource usage"""
        usage = self.generator.get_resource_usage()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        rooms = list(usage.keys())
        bookings = list(usage.values())
        
        ax.bar(rooms, bookings, color='#2563EB')
        ax.set_xlabel('Classroom')
        ax.set_ylabel('Number of Bookings')
        ax.set_title('Resource Usage by Classroom')
        ax.tick_params(axis='x', rotation=45)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_peak_hours(self):
        """Plot peak hours"""
        peak_hours = self.generator.get_peak_hours()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        times = list(peak_hours.keys())
        counts = list(peak_hours.values())
        
        ax.plot(times, counts, marker='o', color='#2563EB', linewidth=2)
        ax.set_xlabel('Time Slot')
        ax.set_ylabel('Number of Bookings')
        ax.set_title('Peak Hours')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        
        self.figure.tight_layout()
        self.canvas.draw()
