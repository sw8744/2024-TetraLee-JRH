import './Description.css';
import { useSearchParams } from 'react-router-dom';
import Header from './Header';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Description() {
    const [searchParams] = useSearchParams();
    const id = searchParams.get('id');
    const clickedFood = searchParams.get('clickedFood');
    const [whereToEat, setWhereToEat] = useState('');
    const [info, setInfo] = useState('');
    const [amount, setAmount] = useState(0);

    const navigate = useNavigate();

    const fetchId = async () => {
        fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            setWhereToEat(data.wheretoeat);
        });
    }

    const getClickedFood = async () => {
        fetch('http://127.0.0.1:5000/api/getfoodinfo/' + clickedFood)
        .then(response => response.json())
        .then(data => {
            setInfo(data[0]);
            console.log(data[0])
        });
    }

    const getAmount = async () => {
        fetch('http://127.0.0.1:5000/api/getfoodamount/' + id + '/' + clickedFood)
        .then(response => response.json())
        .then(data => {
            setAmount(data.amount);
        });
    };

    const plusAmount = () => {
        setAmount(amount + 1);
    };

    const minusAmount = () => {
        setAmount(amount - 1);
    };

    const order = async () => {
        fetch('http://127.0.0.1/api/order/' + id + '/' + clickedFood + '/' + amount,
         {
            method: 'POST'
         }
        )
        .then(response => response.json())
        .then(data => {
            // console.log(data);
        });

        navigate('/menu?id=' + id);
    };

    useEffect(() => {
        fetchId();
        getClickedFood();
        getAmount();
    }, []);

    return (
        <div>
            <Header whereToEat={whereToEat}/>
            <div className='description'>
                <div className='imgDiv'>
                    <img src={info.image} alt='food' className='foodImage'/>
                </div>
                <div className='titleDiv'>
                    <p className='foodName'>{info.name}</p>
                    <p className='price'>{info.price}원</p>
                </div>
                <div className='descDiv'>
                    <p className='title'>메뉴 설명</p>
                    <p className='description_txt'>{info.description}</p>
                    <p className='title'>주의 사항</p>
                    <p className='description_txt'>{info.caution}</p>
                </div>
            </div>
            <div className='buttonDiv'>
                <div className='amountDiv'>
                    <button className='minusButton' onClick={minusAmount}>-</button>
                    <p className='amount'>{amount}</p>
                    <button className='plusButton' onClick={plusAmount}>+</button>
                </div>
                <button className='orderButton' onClick={order}>주문하기</button>
            </div>
            <footer className='footer2'>
                <button className='previousButton'>이전으로</button>
            </footer>
        </div>
    );
};

export default Description;