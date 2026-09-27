(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
    h - block
    i - block
  )
  (:init
    (handempty)
    (clear f)
    (on f g)
    (on g e)
    (on e a)
    (on a i)
    (on i d)
    (on d h)
    (on h b)
    (ontable b)
    (clear c)
    (ontable c)
  )
  (:goal
    (and
      (on g d)
      (on d b)
      (on b c)
      (on c a)
      (on a i)
      (on i f)
      (on f e)
      (on e h)
    )
  )
)
