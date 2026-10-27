# PC Assembly

Вебплатформа для створення власних конфігурацій ПК, а також пошуку, порівняння та купівлі комп'ютерних комплектуючих.

## Functionality

- **Каталог запчастин**: Перегляд списку деталей з можливістю пошуку за назвою, фільтрацією за характеристиками й виробником, а також сортуванням за ціною та популярністю (оцінкою користувачів).

- **Детальна сторінка запчастини**: Перегляд її технічних характеристик, відгуків, оцінок від покупців та додавання власних відгуків.

- **Порівняння**: Можливість обрати кілька деталей одного типу та порівняти їхні характеристики.

- **Конструктор / Збірка ПК**: Можливість поетапно обрати сумісні комплектуючі, зберегти збірку у своєму профілі, переглянути свої збережені збірки та порівняти їх з іншими збірками, або одразу оформити на неї замовлення.

- **Особистий кабінет**: Реєстрація, авторизація, збережені збірки, історія замовлень та редагування особистих даних (нікнейм, ПІБ, номер телефону, пошта, адреса проживання).

- **Панель адміністратора**: Додавання, оновлення та видалення деталей у каталозі, керування статусами замовлень користувачів.


## Endpoints

### Auth

- `POST /auth/register`

  - **Опис:** Реєстрація нового користувача в системі.
  - **Request method:** POST
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "nickname": "pc_master_99",
      "email": "user@example.com",
      "password": "strongPassword123",
      "full_name": "Тарас Шевченко",
      "phone": "+380991234567",
      "address": "м. Київ, вул. Хрещатик, 1"
    }
    ```
  - **Response Status:** `201 Created`, `400 Bad Request`
  - **Response Body (JSON):**
    ```json
    {
      "id": 12,
      "nickname": "pc_master_99",
      "email": "user@example.com",
      "role": "user"
    }
    ```

- `POST /auth/login`

  - **Опис:** Вхід користувача в систему та отримання токена доступу.
  - **Request method:** POST
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "email": "user@example.com",
      "password": "strongPassword123"
    }
    ```
  - **Response Status:** `200 OK`, `401 Unauthorized`
  - **Response Body (JSON):**
    ```json
    {
      "user": {
        "id": 12,
        "nickname": "pc_master_99",
        "role": "user"
      }
    }
    ```

### User Profile

- `GET /users/me`

  - **Опис:** Отримання даних профілю авторизованого користувача.
  - **Request method:** GET
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `401 Unauthorized`
  - **Response Body (JSON):**
    ```json
    {
      "id": 12,
      "nickname": "pc_master_99",
      "full_name": "Тарас Шевченко",
      "email": "user@example.com",
      "phone": "+380991234567",
      "address": "м. Київ, вул. Хрещатик, 1",
      "role": "user"
    }
    ```

- `PATCH /users/me`

  - **Опис:** Оновлення даних профілю авторизованого користувача.
  - **Request method:** PATCH
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "nickname": "pc_master_99",
      "full_name": "Тарас Шевченко",
      "email": "user@example.com",
      "phone": "+380997654321",
      "address": "м. Київ, вул. Лесі Українки, 10"
    }
    ```
  - **Response Status:** `200 OK`, `400 Bad Request`, `401 Unauthorized`
  - **Response Body (JSON):**
    ```json
    {
      "id": 12,
      "nickname": "pc_master_99",
      "full_name": "Тарас Шевченко",
      "email": "user@example.com",
      "phone": "+380997654321",
      "address": "м. Київ, вул. Лесі Українки, 10",
      "role": "user"
    }
    ```

### Parts

- `GET /parts`

  - **Опис:** Отримання списку деталей з підтримкою пагінації, пошуку, фільтрації та сортування.
  - **Request method:** GET
  - **Query Parameters:**
    - `page`: номер сторінки (базово 1)
    - `limit`: кількість об'єктів на сторінці (базово 12)
    - `search`: пошук за назвою (наприклад, `rtx 4070`)
    - `min_price`: мінімальна ціна
    - `max_price`: максимальна ціна
    - `category`: категорія товару (процесора, відеокарта тощо)
    - `sort`: спосіб сортування (по рейтингу, по ціні)
  - **Request body:** порожній
  - **Response Status:** `200 OK`
  - **Response Body (JSON):**
    ```json
    {
      "page": 1,
      "limit": 12,
      "total_items": 45,
      "total_pages": 4,
      "data": [
        {
          "id": 101,
          "title": "AMD Ryzen 7 7800X3D",
          "category": "CPU",
          "price": 17800.00,
          "rating": 4.9,
          "specs": {
            "manufacturer_name": "AMD",
            "socket": "AM5",
            "cores": 8,
            "threads": 16,
            "tdp_watts": 120
          }
        }
      ]
    }
    ```

- `GET /parts/{id}`

  - **Опис:** Отримання повної інформації про конкретну деталь.
  - **Request method:** GET
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `404 Not Found`
  - **Response Body (JSON):**
    ```json
    {
      "id": 101,
      "title": "Intel Core i7-13700K",
      "category": "CPU",
      "price": 16500.00,
      "rating": 4.9,
      "description": "Потужний процесор для ігрових систем та робочих станцій.",
      "specs": {
        "manufacturer_name": "Intel",
        "socket": "LGA1700",
        "cores": 16,
        "threads": 24,
        "base_clock_ghz": 3.4,
        "max_boost_ghz": 5.4,
        "tdp_watts": 125,
        "integrated_graphics": "Intel UHD Graphics 770"
      }
    }
    ```

- `POST /parts`

  - **Опис:** Додавання нової запчастини до каталогу (тільки для роли Admin).
  - **Request method:** POST
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "title": "NVIDIA GeForce RTX 4080 Super",
      "category": "GPU",
      "price": 42000.00,
      "description": "Флагманська відеокарта для 4K геймінгу.",
      "specs": {
        "manufacturer_name": "NVIDIA",
        "vram_gb": 16,
        "interface": "PCIe 4.0",
        "tdp_watts": 320
      }
    }
    ```
  - **Response Status:** `201 Created`, `401 Unauthorized`, `403 Forbidden`
  - **Response Body (JSON):**
    ```json
    {
      "id": 105,
      "title": "NVIDIA GeForce RTX 4080 Super",
      "category": "GPU",
      "price": 42000.00,
      "rating": 0.0,
      "specs": {
        "manufacturer_name": "NVIDIA",
        "vram_gb": 16,
        "interface": "PCIe 4.0",
        "tdp_watts": 320
      }
    }
    ```

- `PATCH /parts/{id}`

  - **Опис:** Оновлення даних запчастини (тільки для роли Admin).
  - **Request method:** PATCH
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "price": 39999.00
    }
    ```
  - **Response Status:** `200 OK`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
  - **Response Body (JSON):**
    ```json
    {
      "id": 105,
      "title": "NVIDIA GeForce RTX 4080 Super",
      "price": 39999.00
    }
    ```

- `DELETE /parts/{id}`

  - **Опис:** Видалення запчастини з каталогу (тільки для роли Admin).
  - **Request method:** DELETE
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `204 No Content`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
  - **Response Body:** порожній

- `GET /parts/compare`

  - **Опис:** Отримання характеристик кількох деталей для їхнього порівняння.
  - **Request method:** GET
  - **Query Parameters:**
    - `ids`: список ID товарів через кому (наприклад, `201,202`)
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `400 Bad Request` (якщо передано товари з різних категорій)
  - **Response Body (JSON):**
    ```json
    {
      "category": "RAM",
      "compared_items": [
        {
          "id": 201,
          "title": "Kingston FURY DDR5 32GB (2x16GB)",
          "price": 5400.00,
          "specs": {
            "manufacturer_name": "Kingston",
            "capacity_gb": 32,
            "memory_type": "DDR5",
            "frequency_mhz": 6000,
            "cas_latency": "CL36"
          }
        },
        {
          "id": 202,
          "title": "Corsair Vengeance DDR5 32GB (2x16GB)",
          "price": 5800.00,
          "specs": {
            "manufacturer_name": "Corsair",
            "capacity_gb": 32,
            "memory_type": "DDR5",
            "frequency_mhz": 6400,
            "cas_latency": "CL32"
          }
        }
      ]
    }
    ```
    
### Reviews

- `GET /parts/{id}/reviews`

  - **Опис:** Отримання переліку відгуків та оцінок для конкретної деталі.
  - **Request method:** GET
  - **Query Parameters:** `page`, `limit`
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `404 Not Found`
  - **Response Body (JSON):**
    ```json
    [
      {
        "id": 1,
        "author": "pc_master_99",
        "rating": 5,
        "comment": "Чудовий процесор, усе працює ідеально!",
        "created_at": "2026-10-10T12:00:00Z"
      }
    ]
    ```

- `POST /parts/{id}/reviews`

  - **Опис:** Додавання нового відгуку та оцінки до товару.
  - **Request method:** POST
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "rating": 5,
      "comment": "Чудовий процесор, усе працює ідеально!"
    }
    ```
  - **Response Status:** `201 Created`, `401 Unauthorized`, `404 Not Found`
  - **Response Body (JSON):**
    ```json
    {
      "id": 1,
      "author": "pc_master_99",
      "rating": 5,
      "comment": "Чудовий процесор, усе працює ідеально!",
      "created_at": "2026-10-10T12:00:00Z"
    }
    ```

### Builds

- `GET /builds`

  - **Опис:** Отримання списку збережених збірок ПК (з підтримкою фільтрації для перегляду власних збірок або збірок інших користувачів).
  - **Request method:** GET
  - **Query Parameters:**
    - `user_id`: ID користувача (необов'язково, використ для перегляду збірок конкретного автора)
    - `page`, `limit`
  - **Request body:** порожній
  - **Response Status:** `200 OK`
  - **Response Body (JSON):**
    ```json
    [
      {
        "id": 42,
        "title": "Ігрова збірка 2026",
        "author": "pc_master_99",
        "total_price": 43800.00,
        "parts_count": 4
      }
    ]
    ```

- `POST /builds`

  - **Опис:** Збереження нової конфігурації ПК (створеної у конструкторі).
  - **Request method:** POST
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "title": "Ігрова збірка 2026",
      "parts": [
        { "part_id": 101, "quantity": 1 },
        { "part_id": 201, "quantity": 2 },
        { "part_id": 305, "quantity": 1 }
      ]
    }
    ```
  - **Response Status:** `201 Created`, `400 Bad Request` (помилка сумісності або некоректні дані), `401 Unauthorized`
  - **Response Body (JSON):**
    ```json
    {
      "id": 42,
      "title": "Ігрова збірка 2026",
      "total_price": 43800.00,
      "parts_count": 4,
      "created_at": "2026-10-13T16:00:00Z"
    }
    ```

- `GET /builds/{id}`

  - **Опис:** Отримання детальної інформації про збережену збірку.
  - **Request method:** GET
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `404 Not Found`
  - **Response Body (JSON):**
    ```json
    {
      "id": 42,
      "title": "Ігрова збірка 2026",
      "author": "pc_master_99",
      "total_price": 43800.00,
      "items": [
        {
          "part_id": 101,
          "title": "Intel Core i7-13700K",
          "category": "CPU",
          "quantity": 1,
          "unit_price": 16500.00
        },
        {
          "part_id": 201,
          "title": "Kingston FURY DDR5 32GB",
          "category": "RAM",
          "quantity": 2,
          "price": 5400.00
        }
      ]
    }
    ```

- `DELETE /builds/{id}`

  - **Опис:** Видалення збереженої збірки користувача.
  - **Request method:** DELETE
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `204 No Content`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
  - **Response Body:** порожній

- `GET /builds/compare`

  - **Опис:** Порівняння кількох збережених збірок ПК між собою.
  - **Request method:** GET
  - **Query Parameters:**
    - `ids`: список ID збірок через кому (наприклад, `42,43`)
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `400 Bad Request`
  - **Response Body (JSON):**
    ```json
    [
      {
        "id": 42,
        "title": "Ігрова збірка 2026",
        "total_price": 43800.00,
        "parts_count": 4
      },
      {
        "id": 43,
        "title": "Бюджетна збірка",
        "total_price": 25000.00,
        "parts_count": 3
      }
    ]
    ```

### Cart

- `GET /cart`

  - **Опис:** Отримання вмісту кошика поточного користувача.
  - **Request method:** GET
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `401 Unauthorized`
  - **Response Body (JSON):**
    ```json
    {
      "items": [
        {
          "cart_item_id": 1,
          "part_id": 101,
          "title": "Intel Core i7-13700K",
          "quantity": 1,
          "price": 16500.00
        }
      ],
      "total_amount": 16500.00
    }
    ```

- `POST /cart/items`

  - **Опис:** Додавання товару до кошика.
  - **Request method:** POST
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "part_id": 101,
      "quantity": 1
    }
    ```
  - **Response Status:** `201 Created`, `401 Unauthorized`, `404 Not Found`
  - **Response Body (JSON):**
    ```json
    {
      "cart_item_id": 1,
      "part_id": 101,
      "quantity": 1,
      "price": 16500.00,
      "total_amount": 16500.00
    }
    ```

- `DELETE /cart/items/{item_id}`

  - **Опис:** Видалення конкретного товару з кошика.
  - **Request method:** DELETE
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `204 No Content`, `401 Unauthorized`, `404 Not Found`
  - **Response Body:** порожній

- `DELETE /cart`

  - **Опис:** Повне очищення кошика поточного користувача.
  - **Request method:** DELETE
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `204 No Content`, `401 Unauthorized`
  - **Response Body:** порожній

### Orders

- `GET /orders`

  - **Опис:** Отримання історії замовлень користувача (або всіх замовлень для Admin).
  - **Request method:** GET
  - **Query Parameters:** `page`, `limit`, `status`
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `401 Unauthorized`
  - **Response Body (JSON):**
    ```json
    [
      {
        "id": 1005,
        "status": "created",
        "total_price": 16500.00,
        "created_at": "2026-10-13T16:30:00Z"
      }
    ]
    ```

- `GET /orders/{id}`

  - **Опис:** Отримання детальної інформації про конкретне замовлення.
  - **Request method:** GET
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `200 OK`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
  - **Response Body (JSON):**
    ```json
    {
      "id": 1005,
      "status": "created",
      "total_price": 16500.00,
      "items": [
        {
          "part_id": 101,
          "title": "Intel Core i7-13700K",
          "quantity": 1,
          "price_at_purchase": 16500.00
        }
      ],
      "created_at": "2026-10-13T16:30:00Z"
    }
    ```

- `POST /orders`

  - **Опис:** Оформлення замовлення на основі товарів, що знаходяться у кошику авторизованого користувача. (Після успішного створення замовлення, кошик автоматично очищується).
  - **Request method:** POST
  - **Query Parameters:** відсутні
  - **Request body:** порожній
  - **Response Status:** `201 Created`, `400 Bad Request` (якщо кошик порожній), `401 Unauthorized`
  - **Response Body (JSON):**
    ```json
    {
      "id": 1005,
      "status": "created",
      "total_price": 16500.00,
      "created_at": "2026-10-13T16:30:00Z"
    }
    ```

- `PATCH /orders/{id}`

  - **Опис:** Оновлення статусу замовлення (доступно лише для користувачів із роллю Admin).
  - **Request method:** PATCH
  - **Query Parameters:** відсутні
  - **Request body (JSON):**
    ```json
    {
      "status": "shipped"
    }
    ```
  - **Response Status:** `200 OK`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
  - **Response Body (JSON):**
    ```json
    {
      "id": 1005,
      "status": "shipped"
    }
    ```
## DB sheme
<img width="729" height="972" alt="DB drawio" src="https://github.com/user-attachments/assets/a5f6041f-2f2d-4802-b08a-0a449b4c3ba5" />

### Як зберігати товари у БД (Архітектурне рішення)

Оскільки комп'ютерні комплектуючі різних типів (процесори, відеокарти, оперативна пам'ять, материнські плати тощо) мають як спільні базові поля, так і зовсім різні технічні характеристики, обрано комбінований підхід із **єдиною таблицею товарів (`Part`), окремими таблицями для категорій (`Category`) і виробників (`Manufacturer`), та `JSONField` для специфічних характеристик (`specs`)**:

1. **Модель `Category`**
   - Зберігає перелік категорій комплектуючих (`CPU`, `GPU`, `RAM`, `Motherboard`, `PSU`, `Storage`, `Case` тощо).
   - **Поля:** `id`, `name` (унікальна назва), `slug`, `description`.
   - **Бізнес-обмеження:** не можна видалити категорію (`on_delete=PROTECT` / статус `409 Conflict`), якщо в базі даних є товари, прив'язані до неї.

2. **Модель `Manufacturer`**
   - Зберігає інформацію про брендів-виробників (`AMD`, `Intel`, `NVIDIA`, `Kingston`, `ASUS` тощо).
   - **Поля:** `id`, `name` (унікальна назва), `country`, `website`, `description`.
   - **Бізнес-обмеження:** не можна видалити виробника (`on_delete=PROTECT` / статус `409 Conflict`), якщо на сайті є закріплені за ним запчастини.

3. **Модель `Part`**
   - Єдина таблиця для всіх комплектуючих, що містить спільні атрибути, за якими найчастіше виконуються пошук, сортування та фільтрація каталогу.
   - **Поля:**
     - `id` — унікальний ідентифікатор;
     - `title` (`CharField`) — назва моделі товару;
     - `category` (`ForeignKey` -> `Category`) — посилання на категорію;
     - `manufacturer` (`ForeignKey` -> `Manufacturer`) — посилання на виробника;
     - `price` (`DecimalField`) — актуальна ціна товару;
     - `stock` (`PositiveIntegerField`) — кількість на складі;
     - `rating` (`DecimalField` / обчислюване поле) — середній рейтинг на основі відгуків;
     - `description` (`TextField`) — текстовий опис деталі;
     - `specs` (`JSONField`) — словник специфічних характеристик залежно від категорії;
     - `created_at`, `updated_at` — часові мітки.

4. **Збереження та валідація `specs` (`JSONField`)**
   - У полі `specs` зберігаються технічні характеристики, специфічні для кожної категорії комплектуючих. Це дозволяє легко перевіряти сумісність деталей при збірці ПК та організувати фільтрацію:
     
     - **CPU (Процесор):**
       ```json
       {
         "socket": "AM5",
         "cores": 8,
         "threads": 16,
         "base_clock_ghz": 4.2,
         "max_boost_ghz": 5.0,
         "tdp_watts": 120,
         "integrated_graphics": "AMD Radeon Graphics"
       }
       ```

     - **Motherboard (Материнська плата):**
       ```json
       {
         "socket": "AM5",
         "chipset": "B650",
         "form_factor": "ATX",
         "memory_type": "DDR5",
         "memory_slots": 4,
         "max_memory_gb": 192,
         "pcie_version": "PCIe 4.0",
         "m2_slots": 3,
         "sata_ports": 4,
         "has_wifi": true
       }
       ```

     - **GPU (Відеокарта):**
       ```json
       {
         "chipset_model": "RTX 4080 Super",
         "vram_gb": 16,
         "memory_type": "GDDR6X",
         "interface": "PCIe 4.0 x16",
         "tdp_watts": 320,
         "recommended_psu_watts": 750,
         "length_mm": 310
       }
       ```

     - **RAM (Оперативна пам'ять):**
       ```json
       {
         "capacity_gb": 32,
         "modules_count": 2,
         "memory_type": "DDR5",
         "frequency_mhz": 6000,
         "cas_latency": "CL36",
         "voltage": 1.35
       }
       ```

     - **Storage (SSD / HDD Накопичувач):**
       ```json
       {
         "type": "NVMe M.2 SSD",
         "form_factor": "M.2 2280",
         "capacity_gb": 1000,
         "interface": "PCIe 4.0 x4",
         "read_speed_mbps": 7400,
         "write_speed_mbps": 6500,
         "tbw": 600
       }
       ```

     - **PSU (Блок живлення):**
       ```json
       {
         "power_watts": 850,
         "form_factor": "ATX",
         "efficiency_rating": "80 PLUS Gold",
         "modularity": "Fully Modular",
         "pcie_connectors": 4
       }
       ```

     - **Case (Корпус):**
       ```json
       {
         "case_type": "Mid-Tower",
         "supported_motherboards": ["ATX", "Micro-ATX", "Mini-ITX"],
         "max_gpu_length_mm": 400,
         "max_cooler_height_mm": 170,
         "included_fans": 3
       }
       ```

     - **Cooler (Кулер / Система охолодження):**
       ```json
       {
         "cooler_type": "Air Cooler",
         "supported_sockets": ["AM4", "AM5", "LGA1700", "LGA1851"],
         "max_tdp_watts": 250,
         "height_mm": 158,
         "fan_size_mm": 120
       }
       ```

   - Валідація структури `specs` виконується на рівні **DRF Serializer** (перевірка обов'язкових ключів та типів значень відповідно до обраної `Category`).


## TODO

- Треба придумати де зберігатися сумісність у БД чи вона буде обчислюватися окремою функцією

- Подумати як саме перевіряти чи користувач зареєстрований

- Подумати як зробити філтрацію за параметрами (характеристиками) деталі

- Подумати де карще зберігати ціни ( у БД одноразово чи використ API для актуальних цін)


