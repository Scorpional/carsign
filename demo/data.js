const demoData = {
  vehicles: [
    { plate: "ABC123", seats: 20, model: "Coach", status: "available", warn: false },
    { plate: "XYZ789", seats: 7, model: "MPV", status: "maintenance", warn: true }
  ],
  staff: [
    { name: "Driver A", role: "driver", phone: "driver@example.com", status: "on_duty", warn: false },
    { name: "Dispatcher A", role: "dispatcher", phone: "disp@example.com", status: "on_duty", warn: false }
  ],
  orders: [
    { customer: "ACME", ride_time: "2025-12-26 09:00", origin: "Point A", destination: "Point B", pax: 10, status: "pending" }
  ],
  dispatch: [
    { trip_code: "20251226-0001", order_id: 1, vehicle: "ABC123", driver: "Driver A", created_at: "2025-12-25 10:00" }
  ],
  trips: [
    { trip_code: "20251226-0001", status: "assigned", accepted_at: "-", departed_at: "-", arrived_at: "-", finished_at: "-" }
  ]
};
