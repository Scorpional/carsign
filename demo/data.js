const demoData = {
  vehicles: [
    { plate: "鄂AUW019", seats: 56, model: "宇通牌", status: "available", warn: false, driver: "容国材 15971455050" },
    { plate: "鄂A33939D", seats: 48, model: "宇通牌", status: "available", warn: false, driver: "雷成元 18661227528" },
    { plate: "鄂ACH877", seats: 48, model: "宇通牌", status: "available", warn: false, driver: "田汉 17507113880" }
  ],
  staff: [
    { name: "容国材", role: "driver", phone: "15971455050", status: "on_duty", warn: false },
    { name: "雷成元", role: "driver", phone: "18661227528", status: "on_duty", warn: false },
    { name: "田汉", role: "driver", phone: "17507113880", status: "on_duty", warn: false }
  ],
  orders: [
    { customer: "美加学院通勤", ride_time: "2025-12-26 08:00", origin: "美加学院", destination: "市区/园区", pax: 48, status: "pending" }
  ],
  dispatch: [
    { trip_code: "20251226-0001", order_id: 1, vehicle: "鄂A33939D", driver: "雷成元", created_at: "2025-12-25 10:00" }
  ],
  trips: [
    { trip_code: "20251226-0001", status: "assigned", accepted_at: "-", departed_at: "-", arrived_at: "-", finished_at: "-" }
  ]
};
