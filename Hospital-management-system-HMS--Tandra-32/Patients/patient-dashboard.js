// Patient Dashboard JavaScript
class PatientDashboard {
    constructor() {
        this.user = null;
        this.appointments = [];
        this.notifications = [];
        this.stats = {};
        this.init();
    }

    async init() {
        await this.checkAuth();
        this.loadComponents();
        this.loadUserData();
        this.loadDashboardData();
        this.setupEventListeners();
        this.setupCharts();
    }

    async checkAuth() {
        try {
            const user = JSON.parse(localStorage.getItem('medfind_user'));
            
            if (!user || user.role !== 'patient') {
                window.location.href = '../public/login.html?redirect=patient-dashboard';
                return;
            }
            
            this.user = user;
            
            // In production, validate token with backend
            // const response = await fetch('/api/auth/validate', {
            //     headers: { 'Authorization': `Bearer ${user.token}` }
            // });
            // if (!response.ok) throw new Error('Invalid token');
            
        } catch (error) {
            console.error('Auth error:', error);
            localStorage.removeItem('medfind_user');
            window.location.href = '../public/login.html';
        }
    }

    loadComponents() {
        // Load navbar
        this.loadComponent('../components/navbar-patient.html', 'navbar-container');
        
        // Load footer
        this.loadComponent('../components/footer.html', 'footer-container');
    }

    async loadComponent(url, containerId) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('Component not found');
            
            const html = await response.text();
            document.getElementById(containerId).innerHTML = html;
            
            // Initialize any scripts in the component
            this.initComponentScripts(containerId);
            
        } catch (error) {
            console.error('Error loading component:', error);
            document.getElementById(containerId).innerHTML = 
                `<div class="alert alert-danger">Error loading component: ${error.message}</div>`;
        }
    }

    initComponentScripts(containerId) {
        const container = document.getElementById(containerId);
        
        // Initialize any interactive elements
        const dropdowns = container.querySelectorAll('.dropdown-toggle');
        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('click', (e) => {
                e.preventDefault();
                const dropdownMenu = dropdown.nextElementSibling;
                dropdownMenu.classList.toggle('show');
            });
        });
        
        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
    }

    async loadUserData() {
        if (!this.user) return;
        
        // Update UI with user data
        this.updateUserInfo();
        
        // Fetch user details from API (mock for now)
        try {
            // In production: const response = await fetch(`/api/patients/${this.user.id}`);
            const userData = {
                name: this.user.name || 'John Doe',
                id: this.user.id || 'PT-12345',
                email: this.user.email,
                phone: this.user.phone,
                avatar: this.user.avatar
            };
            
            this.updateUserInfo(userData);
            
        } catch (error) {
            console.error('Error loading user data:', error);
        }
    }

    updateUserInfo(userData = {}) {
        const name = userData.name || this.user?.name || 'Patient';
        const id = userData.id || this.user?.id || 'PT-00000';
        const avatar = userData.avatar || this.user?.avatar;
        
        // Update avatar with initials
        const initials = name.split(' ').map(n => n[0]).join('').toUpperCase();
        const avatarEl = document.getElementById('userAvatar');
        if (avatarEl) {
            if (avatar) {
                avatarEl.innerHTML = `<img src="${avatar}" alt="${name}" style="width:100%;height:100%;border-radius:50%;">`;
            } else {
                avatarEl.textContent = initials;
            }
        }
        
        // Update name and ID
        const nameEl = document.getElementById('userName');
        const idEl = document.getElementById('patientId');
        const welcomeEl = document.getElementById('welcomeMessage');
        
        if (nameEl) nameEl.textContent = name;
        if (idEl) idEl.textContent = `Patient ID: ${id}`;
        if (welcomeEl) welcomeEl.textContent = `Welcome back, ${name.split(' ')[0]}!`;
    }

    async loadDashboardData() {
        try {
            // Load stats
            await this.loadStats();
            
            // Load appointments
            await this.loadAppointments();
            
            // Load notifications
            await this.loadNotifications();
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data. Please try again.');
        }
    }

    async loadStats() {
        // Mock data - replace with actual API call
        const statsData = {
            upcomingAppointments: 3,
            pendingPrescriptions: 5,
            labReports: 2,
            pendingPayments: 2,
            totalVisits: 24,
            healthScore: 85
        };
        
        this.stats = statsData;
        this.renderStats(statsData);
    }

    renderStats(stats) {
        const statsGrid = document.getElementById('statsGrid');
        if (!statsGrid) return;
        
        const statsHTML = `
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-icon primary">
                        <i class="fas fa-calendar-check"></i>
                    </div>
                    <div class="stat-trend up">
                        <i class="fas fa-arrow-up"></i>
                        12%
                    </div>
                </div>
                <div class="stat-value">${stats.upcomingAppointments}</div>
                <div class="stat-label">Upcoming Appointments</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-icon success">
                        <i class="fas fa-prescription"></i>
                    </div>
                    <div class="stat-trend up">
                        <i class="fas fa-arrow-up"></i>
                        5%
                    </div>
                </div>
                <div class="stat-value">${stats.pendingPrescriptions}</div>
                <div class="stat-label">Active Prescriptions</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-icon warning">
                        <i class="fas fa-file-medical"></i>
                    </div>
                    <div class="stat-trend down">
                        <i class="fas fa-arrow-down"></i>
                        2%
                    </div>
                </div>
                <div class="stat-value">${stats.totalVisits}</div>
                <div class="stat-label">Total Visits</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-icon danger">
                        <i class="fas fa-credit-card"></i>
                    </div>
                    <div class="stat-trend up">
                        <i class="fas fa-arrow-up"></i>
                        15%
                    </div>
                </div>
                <div class="stat-value">৳ 5,200</div>
                <div class="stat-label">Pending Payments</div>
            </div>
        `;
        
        statsGrid.innerHTML = statsHTML;
        
        // Update badges
        this.updateBadges(stats);
    }

    updateBadges(stats) {
        const appointmentBadge = document.getElementById('appointmentBadge');
        const prescriptionBadge = document.getElementById('prescriptionBadge');
        const labReportBadge = document.getElementById('labReportBadge');
        const notificationCount = document.getElementById('notificationCount');
        
        if (appointmentBadge) appointmentBadge.textContent = stats.upcomingAppointments;
        if (prescriptionBadge) prescriptionBadge.textContent = stats.pendingPrescriptions;
        if (labReportBadge) labReportBadge.textContent = stats.labReports;
        if (notificationCount) notificationCount.textContent = this.notifications.filter(n => !n.read).length;
    }

    async loadAppointments() {
        // Mock data - replace with actual API call
        const appointmentsData = [
            {
                id: 'APT-001',
                doctor: 'Dr. Sarah Islam',
                hospital: 'Apollo Hospitals',
                specialty: 'Neurology',
                date: '2024-12-15',
                time: '10:00 AM',
                type: 'video',
                status: 'confirmed'
            },
            {
                id: 'APT-002',
                doctor: 'Dr. Mohammad Rahman',
                hospital: 'Square Hospital',
                specialty: 'Cardiology',
                date: '2024-12-18',
                time: '2:30 PM',
                type: 'in-person',
                status: 'upcoming'
            },
            {
                id: 'APT-003',
                doctor: 'Dr. Kamal Ahmed',
                hospital: 'United Hospital',
                specialty: 'Orthopedics',
                date: '2024-12-22',
                time: '11:00 AM',
                type: 'in-person',
                status: 'upcoming'
            }
        ];
        
        this.appointments = appointmentsData;
        this.renderAppointments(appointmentsData);
    }

    renderAppointments(appointments) {
        const table = document.getElementById('appointmentsTable');
        const emptyState = document.getElementById('noAppointmentsMessage');
        
        if (!appointments || appointments.length === 0) {
            if (table) table.style.display = 'none';
            if (emptyState) emptyState.style.display = 'block';
            return;
        }
        
        if (table) {
            table.style.display = 'table';
            
            const tbody = table.querySelector('tbody') || document.createElement('tbody');
            tbody.innerHTML = '';
            
            appointments.forEach(appointment => {
                const row = this.createAppointmentRow(appointment);
                tbody.appendChild(row);
            });
            
            if (!table.querySelector('tbody')) {
                table.appendChild(tbody);
            }
        }
        
        if (emptyState) {
            emptyState.style.display = 'none';
        }
    }

    createAppointmentRow(appointment) {
        const row = document.createElement('tr');
        row.dataset.id = appointment.id;
        
        const statusClass = `status-${appointment.status}`;
        const statusText = appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1);
        const typeIcon = appointment.type === 'video' ? 'fa-video' : 'fa-hospital';
        const typeText = appointment.type === 'video' ? 'Video Call' : 'In-person';
        
        const date = new Date(appointment.date);
        const now = new Date();
        const diffTime = date - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        let dateText = '';
        if (diffDays === 0) dateText = 'Today';
        else if (diffDays === 1) dateText = 'Tomorrow';
        else if (diffDays < 7) dateText = `In ${diffDays} days`;
        else dateText = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        
        row.innerHTML = `
            <td>
                <div style="font-weight: 600;">${dateText}, ${appointment.time}</div>
                <div style="font-size: 0.875rem; color: var(--gray-500);">${appointment.date}</div>
            </td>
            <td>
                <div style="font-weight: 600;">${appointment.doctor}</div>
                <div style="font-size: 0.875rem; color: var(--gray-500);">${appointment.hospital}</div>
            </td>
            <td>${appointment.specialty}</td>
            <td>
                <span style="display: inline-flex; align-items: center; gap: 0.25rem;">
                    <i class="fas ${typeIcon}" style="color: var(--primary);"></i>
                    ${typeText}
                </span>
            </td>
            <td>
                <span class="appointment-status ${statusClass}">
                    <i class="fas fa-circle"></i>
                    ${statusText}
                </span>
            </td>
            <td>
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-sm btn-light view-appointment-btn" data-id="${appointment.id}">
                        <i class="fas fa-eye"></i>
                    </button>
                    ${appointment.status === 'upcoming' ? `
                        <button class="btn btn-sm btn-light edit-appointment-btn" data-id="${appointment.id}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger cancel-appointment-btn" data-id="${appointment.id}">
                            <i class="fas fa-times"></i>
                        </button>
                    ` : ''}
                </div>
            </td>
        `;
        
        return row;
    }

    async loadNotifications() {
        // Mock data - replace with actual API call
        const notificationsData = [
            {
                id: 'NOT-001',
                type: 'appointment',
                title: 'Appointment Reminder',
                message: 'Your appointment with Dr. Sarah Islam is tomorrow at 10:00 AM',
                time: '2 hours ago',
                read: false,
                icon: 'calendar-alt',
                iconClass: 'info'
            },
            {
                id: 'NOT-002',
                type: 'prescription',
                title: 'New Prescription',
                message: 'Dr. Rahman has prescribed new medications. Check your prescriptions.',
                time: '1 day ago',
                read: true,
                icon: 'prescription',
                iconClass: 'success'
            },
            {
                id: 'NOT-003',
                type: 'payment',
                title: 'Payment Due',
                message: 'Your last consultation bill of ৳ 1,200 is due. Please pay before Dec 20.',
                time: '2 days ago',
                read: true,
                icon: 'file-invoice-dollar',
                iconClass: 'warning'
            }
        ];
        
        this.notifications = notificationsData;
        this.renderNotifications(notificationsData);
    }

    renderNotifications(notifications) {
        const list = document.getElementById('notificationsList');
        const dropdownList = document.getElementById('notificationList');
        const emptyState = document.getElementById('noNotificationsMessage');
        
        if (!notifications || notifications.length === 0) {
            if (list) list.style.display = 'none';
            if (dropdownList) dropdownList.style.display = 'none';
            if (emptyState) emptyState.style.display = 'block';
            return;
        }
        
        // Render main notifications list
        if (list) {
            list.innerHTML = notifications.map(notification => 
                this.createNotificationItem(notification)
            ).join('');
            list.style.display = 'block';
        }
        
        // Render dropdown notifications
        if (dropdownList) {
            dropdownList.innerHTML = notifications.map(notification => 
                this.createDropdownNotificationItem(notification)
            ).join('');
            dropdownList.style.display = 'block';
        }
        
        if (emptyState) {
            emptyState.style.display = 'none';
        }
    }

    createNotificationItem(notification) {
        const unreadClass = !notification.read ? 'unread' : '';
        
        return `
            <div class="notification-item ${unreadClass}" data-id="${notification.id}">
                <div class="notification-icon ${notification.iconClass}">
                    <i class="fas fa-${notification.icon}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">
                        ${notification.title}
                        ${!notification.read ? '<span class="badge badge-primary">New</span>' : ''}
                    </div>
                    <p>${notification.message}</p>
                    <div class="notification-time">
                        <i class="far fa-clock"></i>
                        ${notification.time}
                    </div>
                </div>
            </div>
        `;
    }

    createDropdownNotificationItem(notification) {
        const unreadClass = !notification.read ? 'unread' : '';
        
        return `
            <div class="notification-item ${unreadClass}" data-id="${notification.id}">
                <div class="notification-icon ${notification.iconClass}">
                    <i class="fas fa-${notification.icon}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">${notification.title}</div>
                    <p>${notification.message}</p>
                    <div class="notification-time">${notification.time}</div>
                </div>
            </div>
        `;
    }

    setupCharts() {
        this.setupVisitsChart();
        this.setupExpensesChart();
    }

    setupVisitsChart() {
        const ctx = document.getElementById('visitsChart');
        if (!ctx) return;
        
        // Mock data
        const data = {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Medical Visits',
                data: [2, 3, 1, 4, 2, 1, 3],
                borderColor: 'rgb(37, 99, 235)',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        };
        
        new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: 'var(--gray-500)'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            color: 'var(--gray-500)'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                }
            }
        });
    }

    setupExpensesChart() {
        const ctx = document.getElementById('expensesChart');
        if (!ctx) return;
        
        // Mock data
        const data = {
            labels: ['Consultation', 'Medicines', 'Lab Tests', 'Procedures', 'Others'],
            datasets: [{
                label: 'Amount (BDT)',
                data: [3500, 4200, 1800, 5500, 1200],
                backgroundColor: [
                    'rgba(37, 99, 235, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(139, 92, 246, 0.8)'
                ],
                borderColor: [
                    'rgb(37, 99, 235)',
                    'rgb(16, 185, 129)',
                    'rgb(245, 158, 11)',
                    'rgb(239, 68, 68)',
                    'rgb(139, 92, 246)'
                ],
                borderWidth: 1
            }]
        };
        
        new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `৳${context.raw}`;
                            }
                        },
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '৳' + value;
                            },
                            color: 'var(--gray-500)'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            color: 'var(--gray-500)'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Mobile menu toggle
        const mobileToggle = document.getElementById('mobileMenuToggle');
        const sidebar = document.getElementById('dashboardSidebar');
        
        if (mobileToggle && sidebar) {
            mobileToggle.addEventListener('click', () => {
                sidebar.classList.toggle('active');
            });
            
            // Close sidebar when clicking outside
            document.addEventListener('click', (e) => {
                if (!sidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
                    sidebar.classList.remove('active');
                }
            });
        }
        
        // Logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        }
        
        // Book appointment button
        const bookBtn = document.getElementById('bookAppointmentBtn');
        if (bookBtn) {
            bookBtn.addEventListener('click', () => {
                window.location.href = 'appointment-booking.html';
            });
        }
        
        // Book first appointment button
        const bookFirstBtn = document.getElementById('bookFirstAppointmentBtn');
        if (bookFirstBtn) {
            bookFirstBtn.addEventListener('click', () => {
                window.location.href = 'appointment-booking.html';
            });
        }
        
        // Mark all notifications as read
        const markAllReadBtn = document.getElementById('markAllReadBtn');
        const markNotificationsBtn = document.getElementById('markNotificationsReadBtn');
        
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.markAllNotificationsAsRead();
            });
        }
        
        if (markNotificationsBtn) {
            markNotificationsBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.markAllNotificationsAsRead();
            });
        }
        
        // Notification click handlers
        document.addEventListener('click', (e) => {
            const notificationItem = e.target.closest('.notification-item');
            if (notificationItem) {
                const notificationId = notificationItem.dataset.id;
                this.handleNotificationClick(notificationId);
            }
        });
        
        // Appointment action handlers
        document.addEventListener('click', (e) => {
            if (e.target.closest('.view-appointment-btn')) {
                const appointmentId = e.target.closest('.view-appointment-btn').dataset.id;
                this.viewAppointment(appointmentId);
            }
            
            if (e.target.closest('.edit-appointment-btn')) {
                const appointmentId = e.target.closest('.edit-appointment-btn').dataset.id;
                this.editAppointment(appointmentId);
            }
            
            if (e.target.closest('.cancel-appointment-btn')) {
                const appointmentId = e.target.closest('.cancel-appointment-btn').dataset.id;
                this.showCancelModal(appointmentId);
            }
        });
        
        // Modal handlers
        const modal = document.getElementById('appointmentModal');
        const modalClose = modal?.querySelector('.modal-close');
        const cancelModalBtn = document.getElementById('cancelModalBtn');
        const confirmCancelBtn = document.getElementById('confirmCancelBtn');
        
        if (modalClose) {
            modalClose.addEventListener('click', () => {
                modal.classList.remove('active');
            });
        }
        
        if (cancelModalBtn) {
            cancelModalBtn.addEventListener('click', () => {
                modal.classList.remove('active');
            });
        }
        
        if (confirmCancelBtn) {
            confirmCancelBtn.addEventListener('click', () => {
                const appointmentId = confirmCancelBtn.dataset.appointmentId;
                this.cancelAppointment(appointmentId);
                modal.classList.remove('active');
            });
        }
        
        // Close modal when clicking outside
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        }
        
        // Time range change handlers
        const visitsRange = document.getElementById('visitsTimeRange');
        const expensesRange = document.getElementById('expensesTimeRange');
        
        if (visitsRange) {
            visitsRange.addEventListener('change', () => {
                this.refreshVisitsChart(visitsRange.value);
            });
        }
        
        if (expensesRange) {
            expensesRange.addEventListener('change', () => {
                this.refreshExpensesChart(expensesRange.value);
            });
        }
        
        // Window resize handler
        window.addEventListener('resize', () => {
            // Update charts on resize
            this.refreshCharts();
        });
    }

    async logout() {
        if (confirm('Are you sure you want to logout?')) {
            try {
                // In production: await fetch('/api/auth/logout', { method: 'POST' });
                localStorage.removeItem('medfind_user');
                window.location.href = '../public/index.html';
            } catch (error) {
                console.error('Logout error:', error);
                // Force logout anyway
                localStorage.removeItem('medfind_user');
                window.location.href = '../public/index.html';
            }
        }
    }

    async markAllNotificationsAsRead() {
        try {
            // In production: await fetch('/api/notifications/mark-all-read', { method: 'POST' });
            
            this.notifications.forEach(notification => {
                notification.read = true;
            });
            
            this.renderNotifications(this.notifications);
            this.updateNotificationCount();
            
            this.showSuccess('All notifications marked as read');
            
        } catch (error) {
            console.error('Error marking notifications as read:', error);
            this.showError('Failed to mark notifications as read');
        }
    }

    async handleNotificationClick(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (!notification) return;
        
        // Mark as read
        notification.read = true;
        
        // Update UI
        this.renderNotifications(this.notifications);
        this.updateNotificationCount();
        
        // Navigate based on notification type
        switch (notification.type) {
            case 'appointment':
                window.location.href = 'appointment-booking.html';
                break;
            case 'prescription':
                window.location.href = '../prescriptions.html';
                break;
            case 'payment':
                window.location.href = '../billing.html';
                break;
            default:
                // Do nothing
                break;
        }
    }

    updateNotificationCount() {
        const unreadCount = this.notifications.filter(n => !n.read).length;
        const badge = document.getElementById('notificationCount');
        if (badge) {
            badge.textContent = unreadCount;
            badge.style.display = unreadCount > 0 ? 'flex' : 'none';
        }
    }

    async viewAppointment(appointmentId) {
        const appointment = this.appointments.find(a => a.id === appointmentId);
        if (appointment) {
            // In production, navigate to appointment details page
            alert(`Viewing appointment: ${appointment.doctor} - ${appointment.date}`);
        }
    }

    async editAppointment(appointmentId) {
        const appointment = this.appointments.find(a => a.id === appointmentId);
        if (appointment) {
            // In production, open edit modal or navigate to edit page
            alert(`Editing appointment: ${appointment.doctor} - ${appointment.date}`);
        }
    }

    showCancelModal(appointmentId) {
        const appointment = this.appointments.find(a => a.id === appointmentId);
        if (!appointment) return;
        
        const modal = document.getElementById('appointmentModal');
        const detailsEl = document.getElementById('cancelAppointmentDetails');
        const confirmBtn = document.getElementById('confirmCancelBtn');
        
        if (detailsEl) {
            detailsEl.innerHTML = `
                <p><strong>Doctor:</strong> ${appointment.doctor}</p>
                <p><strong>Date:</strong> ${appointment.date} at ${appointment.time}</p>
                <p><strong>Hospital:</strong> ${appointment.hospital}</p>
                <p><strong>Type:</strong> ${appointment.type === 'video' ? 'Video Call' : 'In-person'}</p>
            `;
        }
        
        if (confirmBtn) {
            confirmBtn.dataset.appointmentId = appointmentId;
        }
        
        if (modal) {
            modal.classList.add('active');
        }
    }

    async cancelAppointment(appointmentId) {
        try {
            // In production: await fetch(`/api/appointments/${appointmentId}/cancel`, { method: 'POST' });
            
            // Update local state
            const appointment = this.appointments.find(a => a.id === appointmentId);
            if (appointment) {
                appointment.status = 'cancelled';
                this.renderAppointments(this.appointments);
            }
            
            this.showSuccess('Appointment cancelled successfully');
            
            // Update stats
            this.loadStats();
            
        } catch (error) {
            console.error('Error cancelling appointment:', error);
            this.showError('Failed to cancel appointment');
        }
    }

    refreshVisitsChart(timeRange) {
        // In production, fetch new data based on time range
        console.log('Refreshing visits chart with range:', timeRange);
        // this.setupVisitsChart();
    }

    refreshExpensesChart(timeRange) {
        // In production, fetch new data based on time range
        console.log('Refreshing expenses chart with range:', timeRange);
        // this.setupExpensesChart();
    }

    refreshCharts() {
        // Re-initialize charts on window resize
        this.setupCharts();
    }

    showSuccess(message) {
        this.showToast(message, 'success');
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="toast-close">&times;</button>
        `;
        
        // Add to page
        document.body.appendChild(toast);
        
        // Remove after 5 seconds
        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 5000);
        
        // Close button
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                toast.classList.add('fade-out');
                setTimeout(() => {
                    if (toast.parentNode) {
                        toast.parentNode.removeChild(toast);
                    }
                }, 300);
            });
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PatientDashboard();
});