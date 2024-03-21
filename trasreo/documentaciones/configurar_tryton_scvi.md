# Configuración de un tryton

```bash
ssh admon@200.116.93.156 -L 8001:localhost:8001
```


### Descripción
- Este triton puede administratr terceros, clientes o proveedores. 
- Puede hacer gestion de produtos
- Maneja compras ventas
- Manejo de investarios
- Todo lo anterior para multiples almacenes o bodegas
- Al final todo esto llega al punto de la contabilidad (Colombiana)

# Centro Taller Recreo


### 1. Montar la instancia (od-docker)

### 2. Se empieza  a hacer las configuracion inicial
- consiste en configurar los modulos que se vana  utilizar

Los modulos que se van a ativas son:
    - sales
        # El resto son dependencias de este modulo
    - sale_pos (punto de venta)
        # El resto son dependencias de este modulo
    - purchase
    - account_stock_continental
    - account_co_co # Especifico de la contabilidad colombiana
    - account_co_pyme
    - account_co_reports 
```

```

## 1. Entender la dinamica del negocio y Diseno de la solucion
- Esto implica definir cuales seran lo modulos que se van a implementar
- implica entender cuales es el problema o necesidades a solucionar


## 2. Desarrollar y realizar el despliego
- Con los modelos que ya estan construidos y sirven en su totalidad o parte de el, empiezo a construir la solucion, que implica mas desarrollo. Crear un modulo o implementar muchos modulos. 

## 3. Realizar un entrega de un producto

- Poner en produccion un servicio que es el que el cliente va a utilizar
