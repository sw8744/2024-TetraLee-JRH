import Header from "./Header";
import { useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import './HowToPay.css';

function HowToPay() {
    const [searchParams] = useSearchParams();
    const [whereToEat, setWhereToEat] = useState('');
    const id = searchParams.get('id');
    const navigate = useNavigate();

    const fetchId = async () => {
        fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            setWhereToEat(data.wheretoeat);
        });
    };

    const cancel = () => {
        navigate('/menu?id=' + id);
    };

    useEffect(() => {
        fetchId();
    }, []);

    return (
        <>
            <Header whereToEat={whereToEat}/>
            <div className="payButtonDiv">
                <button className="payNow">바로 결제</button>
                <button className="point">포인트 적립</button>
                <button className="coupon">쿠폰 사용</button>
            </div>
            <footer className='footer2'>
                <button className='cancelButton2' onClick={() => {cancel()}}>이전으로</button>
            </footer>
        </>
    );
}

export default HowToPay;